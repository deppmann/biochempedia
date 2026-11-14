"""Two Genes, Sixteen Chances.

COLOR MAP (continued exactly from chapter 1)
  PURPLE = dominant alleles (R, Y)
  WHITE  = recessive alleles (r, y)
  GREEN  = Punnett grids and model boundaries
  YELLOW = chance, paths, and probability markers
  TEAL   = neutral teaching labels
"""
from bp_parts import *  # noqa: F401,F403

PURPLE = "#B58CD9"
WHITE = "#FFFFFF"
GRID = GREEN
CHANCE = YELLOW

GAMETES = ("RY", "Ry", "rY", "ry")


class FilmScene(SpokenScene):
    """Shared diagram field: a full-height board and gently moving chance markers."""
    def setup(self):
        super().setup()
        board = RoundedRectangle(corner_radius=0.35, width=12.65, height=6.85,
                                 stroke_color=TEAL, stroke_width=2,
                                 fill_color="#24344A", fill_opacity=0.92)
        board.layout_ok = True  # decorative field intentionally sits behind all diagram text
        board.set_z_index(-20)
        self.add(board)
        motes = VGroup()
        for i in range(12):
            x = -5.7 + (i % 6) * 2.25
            y = -2.95 if i < 6 else 2.95
            d = Dot([x, y, 0], radius=0.13, color=CHANCE).set_opacity(0.20)
            d.v = (0.16 + 0.025 * (i % 3)) * (1 if i < 6 else -1)
            def drift(m, dt):
                m.shift(RIGHT * m.v * dt)
                if m.get_x() > 6.0: m.set_x(-6.0)
                if m.get_x() < -6.0: m.set_x(6.0)
            d.add_updater(drift)
            motes.add(d)
        motes.set_z_index(-10)
        self.add(motes)


def allele(letter, size=0.64):
    """One allele card; capitals use chapter 1 purple, lowercase white."""
    col = PURPLE if letter.isupper() else WHITE
    box = RoundedRectangle(corner_radius=0.12, width=size, height=size,
                           stroke_color=col, stroke_width=3,
                           fill_color=col, fill_opacity=0.88)
    txt = T(letter, max(24, int(size * 42)), BG, weight=BOLD).move_to(box)
    txt.layout_ok = True
    return VGroup(box, txt)


def gamete(label, center=ORIGIN, radius=0.48, hidden=False):
    """Sex-cell circle with exactly one shape and one colour allele."""
    c = Circle(radius=radius, stroke_color=TEAL, stroke_width=3,
               fill_color=TEAL, fill_opacity=0.10).move_to(center)
    if hidden:
        q = T("?", 34, TEAL, weight=BOLD).move_to(c)
        q.layout_ok = True  # traveling chance dots deliberately stop on these hidden cards
        return VGroup(c, q)
    a = allele(label[0], 0.38)
    b = allele(label[1], 0.38)
    pair = VGroup(a, b).arrange(RIGHT, buff=0.08).move_to(c)
    return VGroup(c, pair)


def seed(kind="round", color="yellow", height=0.82):
    """Large schematic pea seed: shape and fill encode the two traits."""
    fill = CHANCE if color == "yellow" else GREEN
    if kind == "round":
        body = Circle(radius=0.5, stroke_color=fill, stroke_width=3,
                      fill_color=fill, fill_opacity=0.82)
    else:
        pts = []
        for i in range(16):
            a = TAU * i / 16
            r = 0.50 if i % 2 == 0 else 0.38
            pts.append([r * np.cos(a), r * np.sin(a), 0])
        body = Polygon(*pts, stroke_color=fill, stroke_width=3,
                       fill_color=fill, fill_opacity=0.82)
    body.set_height(height)
    shine = Dot(body.get_center() + UL * height * 0.16, radius=height * 0.045,
                color=WHITE).set_opacity(0.75)
    return VGroup(body, shine)


def parent_diagram(center=ORIGIN, label="parent"):
    """The carried parent: R/r row over Y/y row, at a fixed scale."""
    frame = RoundedRectangle(corner_radius=0.35, width=3.6, height=3.5,
                             stroke_color=TEAL, stroke_width=3,
                             fill_color=TEAL, fill_opacity=0.07).move_to(center)
    title = T(label, 30, TEAL, weight=BOLD).next_to(frame, UP, buff=0.14)
    rr = VGroup(allele("R"), allele("r")).arrange(RIGHT, buff=0.35)
    yy = VGroup(allele("Y"), allele("y")).arrange(RIGHT, buff=0.35)
    rows = VGroup(rr, yy).arrange(DOWN, buff=0.55).move_to(frame)
    return VGroup(frame, title, rows)


def choice_tree(hidden=False):
    """Fixed two-gene choice tree used unchanged in scenes 4 through 7."""
    root = Dot([-5.25, 0.25, 0], radius=0.11, color=TEAL)
    shape_pts = [np.array([-2.65, 1.75, 0]), np.array([-2.65, -1.25, 0])]
    leaf_pts = [np.array([1.15, 2.35, 0]), np.array([1.15, 1.15, 0]),
                np.array([1.15, -0.65, 0]), np.array([1.15, -1.85, 0])]
    branches = VGroup()
    for p in shape_pts:
        branches.add(Line(root.get_center(), p, color=CHANCE, stroke_width=5))
    for i, p in enumerate(shape_pts):
        branches.add(Line(p, leaf_pts[2*i], color=CHANCE, stroke_width=5),
                     Line(p, leaf_pts[2*i+1], color=CHANCE, stroke_width=5))
    shape_cards = VGroup(allele("R").move_to(shape_pts[0]), allele("r").move_to(shape_pts[1]))
    color_cards = VGroup(allele("Y", 0.58).move_to([-0.55, 2.35, 0]),
                         allele("y", 0.58).move_to([-0.55, 1.15, 0]),
                         allele("Y", 0.58).move_to([-0.55, -0.65, 0]),
                         allele("y", 0.58).move_to([-0.55, -1.85, 0]))
    cells = VGroup(*[gamete(g, p + RIGHT * 1.05, hidden=hidden)
                     for g, p in zip(GAMETES, leaf_pts)])
    return VGroup(root, branches, shape_cards, color_cards, cells)


def cross_genotype(a, b):
    """Combine two gamete strings gene-by-gene, dominant allele first."""
    pair = lambda x, y: "".join(sorted((x, y), key=lambda z: z.islower()))
    return pair(a[0], b[0]) + pair(a[1], b[1])


def phenotype(genotype):
    return ("round" if "R" in genotype[:2] else "wrinkled",
            "yellow" if "Y" in genotype[2:] else "green")


def punnett_grid(show_genotypes=True, show_seeds=False, opacity=1.0):
    """The one carried 4x4 grid; all later scenes call this exact builder."""
    cell = 1.15
    x0, y0 = -1.45, 1.60
    lines = VGroup()
    for k in range(5):
        lines.add(Line([x0 + k*cell, y0, 0], [x0 + k*cell, y0 - 4*cell, 0],
                       color=GRID, stroke_width=3),
                  Line([x0, y0 - k*cell, 0], [x0 + 4*cell, y0 - k*cell, 0],
                       color=GRID, stroke_width=3))
    top = VGroup(*[T(g, 27, TEXT, weight=BOLD).move_to([x0+(i+0.5)*cell, y0+0.43, 0])
                   for i, g in enumerate(GAMETES)])
    side = VGroup(*[T(g, 27, TEXT, weight=BOLD).move_to([x0-0.48, y0-(j+0.5)*cell, 0])
                    for j, g in enumerate(GAMETES)])
    contents = VGroup()
    for j, row in enumerate(GAMETES):
        for i, col in enumerate(GAMETES):
            gt = cross_genotype(col, row)
            pos = [x0+(i+0.5)*cell, y0-(j+0.5)*cell, 0]
            if show_seeds:
                s = seed(*phenotype(gt), height=0.55).move_to(pos)
                if show_genotypes:
                    lab = T(gt, 16, TEXT).next_to(s, DOWN, buff=0.02)
                    lab.layout_ok = True
                    contents.add(VGroup(s, lab))
                else:
                    contents.add(s)
            elif show_genotypes:
                contents.add(T(gt, 28, TEXT, weight=BOLD).move_to(pos))
    g = VGroup(lines, top, side, contents).set_opacity(opacity)
    g.lines, g.top, g.side, g.contents = lines, top, side, contents
    return g


def mini_grid(n=2, center=ORIGIN, size=2.4):
    lines = VGroup()
    x0, y0 = center[0]-size/2, center[1]+size/2
    for k in range(n+1):
        lines.add(Line([x0+k*size/n, y0, 0], [x0+k*size/n, y0-size, 0], color=GRID, stroke_width=3),
                  Line([x0, y0-k*size/n, 0], [x0+size, y0-k*size/n, 0], color=GRID, stroke_width=3))
    return lines


class S00Hook(TitleCard, SpokenScene):
    LESSON = "Mendel and Punnett squares"
    TITLE = "Two Genes, Sixteen Chances"

    def construct(self):
        old = mini_grid(2, center=[-2.8, -0.1, 0], size=3.6)
        heads = VGroup(T("P", 32, PURPLE), T("p", 32, WHITE)).arrange(RIGHT, buff=1.25).move_to([-2.8, 2.25, 0])
        self.play(Create(old), FadeIn(heads), run_time=0.8)
        self.at("What changes")
        q = fit_text("What changes when two genes travel together?", max_w=5.5, size=36, color=CHANCE)
        q.move_to([3.3, 1.2, 0])
        self.play(FadeIn(q, shift=UP*0.2), run_time=0.6)
        self.at("The grid must")
        second = VGroup(allele("R"), allele("r"), allele("Y"), allele("y")).arrange(RIGHT, buff=0.18)
        second.move_to([3.25, -0.6, 0])
        stretch = old.copy().stretch(1.55, 0).move_to([-1.8, -0.1, 0])
        self.play(FadeOut(q), Transform(old, stretch),
                  LaggedStart(*[FadeIn(x, shift=UP*0.2) for x in second], lag_ratio=0.15), run_time=1.6)
        pulse(old, base=3, amp=1.0, speed=2)
        self.finish()


class S01Title(TitleCard):
    LESSON = "Mendel and Punnett squares"
    TITLE = "Two Genes, Sixteen Chances"


class S02Traits(FilmScene):
    def construct(self):
        tp = TwoPanel("seed shape", "seed color", colors=(PURPLE, CHANCE), top=3.0, bottom=-2.8)
        self.play(FadeIn(tp), run_time=0.7)
        round_s, wrinkle_s = seed("round", "green", 1.45), seed("wrinkled", "green", 1.45)
        round_s.move_to([-4.6, 0.6, 0]); wrinkle_s.move_to([-1.8, 0.6, 0])
        yellow_s, green_s = seed("round", "yellow", 1.45), seed("round", "green", 1.45)
        yellow_s.move_to([1.8, 0.6, 0]); green_s.move_to([4.6, 0.6, 0])
        self.play(LaggedStart(*[FadeIn(x, scale=0.8) for x in (round_s, wrinkle_s, yellow_s, green_s)], lag_ratio=0.15), run_time=1.5)
        self.at("capital R")
        labs1 = VGroup(T("R  round", 30, PURPLE), T("r  wrinkled", 30, WHITE)).arrange(RIGHT, buff=0.55).move_to([-3.2, -1.25, 0])
        self.play(FadeIn(labs1), run_time=0.6)
        self.at("Capital Y")
        labs2 = VGroup(T("Y  yellow", 30, PURPLE), T("y  green", 30, WHITE)).arrange(RIGHT, buff=0.55).move_to([3.2, -1.25, 0])
        self.play(FadeIn(labs2), run_time=0.6)
        bob(round_s, amp=0.07); bob(wrinkle_s, amp=0.07, seed=1)
        bob(yellow_s, amp=0.07, seed=2); bob(green_s, amp=0.07, seed=3)
        self.finish()


class S03Parent(FilmScene):
    def construct(self):
        left = parent_diagram([-3.2, 0.1, 0], "parent 1")
        right = parent_diagram([3.2, 0.1, 0], "parent 2")
        self.play(FadeIn(left), FadeIn(right), run_time=1.0)
        self.at("Every sex cell")
        out = VGroup(gamete("RY", [-3.2, -2.65, 0]), gamete("ry", [3.2, -2.65, 0]))
        arrows = VGroup(Arrow([-3.2,-1.2,0],[-3.2,-2.05,0],buff=0.05,color=CHANCE),
                        Arrow([3.2,-1.2,0],[3.2,-2.05,0],buff=0.05,color=CHANCE))
        self.play(GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=0.5)
        self.play(FadeIn(out), run_time=0.7)
        bob(out[0], amp=0.06); bob(out[1], amp=0.06, seed=2)
        self.finish()


class S04Independent(FilmScene):
    def construct(self):
        tree = choice_tree(hidden=False)
        self.play(FadeIn(tree[0]), Create(VGroup(*tree[1][:2])), FadeIn(tree[2]), run_time=1.0)
        self.add(scope_tag("schematic"))
        self.at("Receiving either")
        self.play(Create(VGroup(*tree[1][2:])), FadeIn(tree[3]), run_time=1.6)
        self.at("That creates")
        self.play(LaggedStart(*[FadeIn(c, shift=RIGHT*0.25) for c in tree[4]], lag_ratio=0.15), run_time=1.2)
        for i, c in enumerate(tree[4]): bob(c, amp=0.05, seed=i)
        self.finish()


class S05Predict(FilmScene):
    def construct(self):
        tree = choice_tree(hidden=True)
        self.add(tree, scope_tag("schematic"))
        q = question_card("How many sex-cell types can this parent make?", y=-3.2, size=30)
        self.play(FadeIn(q.question), run_time=0.6)
        self.at("Follow every path")
        dots = VGroup(*[Dot([-5.25,0.25,0], radius=0.12, color=CHANCE) for _ in range(4)])
        self.add(dots)
        targets = [c.get_center() for c in tree[4]]
        self.play(*[dots[i].animate.move_to(targets[i]) for i in range(4)], run_time=2.4, rate_func=linear)
        for d in dots: pulse(d, base=1, amp=1, speed=3)
        self.finish()


class S06Pause(PredictPause):
    QUESTION = "How many sex-cell types can this parent make?"
    SECONDS = 4.5
    CARD = {"y": -3.2, "size": 30}
    def backdrop(self):
        return choice_tree(hidden=True)

    def construct(self):
        tree = self.backdrop()
        self.add(tree)
        self.add(question_card(self.QUESTION, y=-3.2, size=30))
        ring, run = countdown(self.SECONDS, center=self.RING_AT)
        self.add(ring)
        movers = VGroup(*[Dot(c.get_center(), radius=0.13, color=CHANCE) for c in tree[4]])
        self.add(movers)
        arcs = [Arc(radius=0.22, start_angle=i*PI/2, angle=TAU,
                    arc_center=c.get_center()) for i,c in enumerate(tree[4])]
        self.play(run, *[MoveAlongPath(m, a, rate_func=linear) for m,a in zip(movers,arcs)],
                  run_time=self.SECONDS, rate_func=linear)
        self.finish()


class S07Reveal(FilmScene):
    def construct(self):
        hidden = choice_tree(hidden=True)
        self.add(hidden[0], hidden[1], hidden[2], hidden[3], scope_tag("schematic"))
        leaves = hidden[4]
        self.add(leaves)
        shown = choice_tree(hidden=False)[4]
        phrases = ("capital R capital Y", "capital R small y", "small r capital Y", "small r small y")
        for i, phrase in enumerate(phrases):
            self.at(phrase)
            self.play(Transform(leaves[i], shown[i]), run_time=0.55)
        self.at("Each type")
        probs = VGroup(*[T("1/4", 25, CHANCE).next_to(c, RIGHT, buff=0.12) for c in leaves])
        self.play(LaggedStart(*[FadeIn(x) for x in probs], lag_ratio=0.12), run_time=0.8)
        for i, c in enumerate(leaves): bob(c, amp=0.05, seed=i)
        self.finish()


class S07Complete(FilmScene):
    def construct(self):
        good = VGroup(*[gamete(g, [-4.5 + i*3, 1.2, 0], radius=0.62) for i,g in enumerate(GAMETES)])
        self.play(LaggedStart(*[FadeIn(c, scale=0.8) for c in good], lag_ratio=0.15), run_time=1.4)
        self.at("No path")
        bad1 = VGroup(Circle(0.62, color=RED), allele("R",0.42), allele("R",0.42)).arrange(RIGHT,buff=0.05).move_to([-1.6,-1.4,0])
        bad2 = VGroup(Circle(0.62, color=RED), allele("Y",0.42), allele("y",0.42)).arrange(RIGHT,buff=0.05).move_to([1.6,-1.4,0])
        crosses = VGroup(T("×", 54, RED).move_to(bad1), T("×",54,RED).move_to(bad2))
        self.play(FadeIn(bad1), FadeIn(bad2), run_time=0.7)
        self.play(FadeIn(crosses, scale=1.3), run_time=0.5)
        for i,c in enumerate(good): bob(c, amp=0.05, seed=i)
        self.finish()


class S08Expand(FilmScene):
    def construct(self):
        g = punnett_grid(show_genotypes=False)
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN*0.2) for x in g.top], lag_ratio=0.12),
                  LaggedStart(*[FadeIn(x, shift=RIGHT*0.2) for x in g.side], lag_ratio=0.12), run_time=1.5)
        self.at("The square expands")
        self.play(Create(g.lines), run_time=1.4)
        full = punnett_grid(show_genotypes=True)
        self.at("Each box")
        self.play(LaggedStart(*[FadeIn(x, scale=0.7) for x in full.contents], lag_ratio=0.08), run_time=2.4)
        self.finish()


class S08Read(FilmScene):
    def construct(self):
        row = gamete("rY", [-3.8, 1.1, 0], radius=0.65)
        col = gamete("Ry", [3.8, 1.1, 0], radius=0.65)
        box = RoundedRectangle(corner_radius=0.2,width=3.0,height=2.2,color=GRID,stroke_width=4).move_to([0,-0.3,0])
        self.play(FadeIn(row), FadeIn(col), Create(box), run_time=1.0)
        self.at("Combine the shape")
        shape = T("Rr", 50, PURPLE, weight=BOLD).move_to([-0.65,-0.3,0])
        self.play(row.animate.move_to([-2.4,-0.3,0]), col.animate.move_to([2.4,-0.3,0]), FadeIn(shape), run_time=1.0)
        self.at("then the color")
        colour = T("Yy", 50, PURPLE, weight=BOLD).move_to([0.65,-0.3,0])
        self.play(FadeIn(colour), run_time=0.6)
        self.at("The finished genotype")
        pea = seed("round","yellow",1.3).move_to([0,-2.4,0])
        self.play(FadeIn(pea, scale=0.7), run_time=0.7)
        bob(pea, amp=0.07)
        self.finish()


class S09Group(FilmScene):
    def construct(self):
        grid = punnett_grid(show_genotypes=True, show_seeds=False)
        self.add(grid)
        self.at("group boxes")
        seed_grid = punnett_grid(show_genotypes=True, show_seeds=True)
        self.play(Transform(grid.contents, seed_grid.contents), run_time=1.8)
        self.at("dominant shape")
        round_marks = VGroup(*[SurroundingRectangle(seed_grid.contents[i][0], color=PURPLE, buff=0.04)
                               for i in range(16) if phenotype(cross_genotype(GAMETES[i%4],GAMETES[i//4]))[0]=="round"])
        for mark in round_marks: mark.layout_ok = True  # deliberate phenotype highlight around seed + faint genotype
        self.play(LaggedStart(*[Create(x) for x in round_marks], lag_ratio=0.03), run_time=1.0)
        self.at("dominant color")
        self.play(FadeOut(round_marks), run_time=0.4)
        yellow_marks = VGroup(*[SurroundingRectangle(seed_grid.contents[i][0], color=CHANCE, buff=0.04)
                                for i in range(16) if phenotype(cross_genotype(GAMETES[i%4],GAMETES[i//4]))[1]=="yellow"])
        for mark in yellow_marks: mark.layout_ok = True  # deliberate phenotype highlight around seed + faint genotype
        self.play(LaggedStart(*[Create(x) for x in yellow_marks], lag_ratio=0.03), run_time=1.0)
        self.finish()


def phenotype_bins():
    specs = [("round yellow",9,"9/16","round","yellow"),
             ("round green",3,"3/16","round","green"),
             ("wrinkled yellow",3,"3/16","wrinkled","yellow"),
             ("wrinkled green",1,"1/16","wrinkled","green")]
    xs = [-4.8,-1.6,1.6,4.8]
    groups = VGroup()
    for x,(name,n,frac,sh,col) in zip(xs,specs):
        frame = RoundedRectangle(corner_radius=0.18,width=2.65,height=4.8,color=GRID,stroke_width=3).move_to([x,0,0])
        lab = fit_text(name,max_w=2.35,size=28,color=TEXT,max_lines=2).move_to([x,1.85,0])
        icon = seed(sh,col,0.9).move_to([x,0.55,0])
        num = M(str(n),46,CHANCE).move_to([x,-0.65,0])
        f = M(frac,28,TEXT).move_to([x,-1.5,0])
        groups.add(VGroup(frame,lab,icon,num,f))
    return groups


class S10Ratio(FilmScene):
    def construct(self):
        bins = phenotype_bins()
        self.play(FadeIn(bins[0]), run_time=0.8)
        self.at("Two smaller")
        self.play(FadeIn(bins[1]), FadeIn(bins[2]), run_time=0.9)
        self.at("The smallest")
        self.play(FadeIn(bins[3]), run_time=0.6)
        ratio = M("9 : 3 : 3 : 1", 42, CHANCE).move_to([0,-3.15,0])
        self.play(FadeIn(ratio), run_time=0.7)
        for i,b in enumerate(bins): bob(b[2], amp=0.05, seed=i)
        self.finish()


class S10Rare(FilmScene):
    def construct(self):
        g = punnett_grid(show_genotypes=True, show_seeds=True, opacity=0.28)
        self.add(g)
        idx = 15
        rare = g.contents[idx]
        rare.set_opacity(1)
        highlight = SurroundingRectangle(rare, color=CHANCE, buff=0.08, stroke_width=5)
        self.play(Create(highlight), run_time=0.8)
        self.at("recessive alleles")
        label = T("rryy", 38, WHITE, weight=BOLD).move_to([4.5,1.9,0])
        arrow = Arrow(label.get_left(), highlight.get_right(), buff=0.15,color=CHANCE)
        self.play(FadeIn(label), GrowArrow(arrow), run_time=0.8)
        self.at("That combination")
        traces = VGroup(Dot(g.top[3].get_center(), radius=0.14, color=CHANCE),
                        Dot(g.side[3].get_center(), radius=0.14, color=CHANCE))
        self.add(traces)
        context_cells = VGroup(*[c for i,c in enumerate(g.contents) if i != idx])
        self.play(traces[0].animate.move_to(rare.get_center()),
                  traces[1].animate.move_to(rare.get_center()),
                  g.lines.animate.set_opacity(0.10),
                  context_cells.animate.set_opacity(0.10),
                  g.top.animate.set_opacity(0.10), g.side.animate.set_opacity(0.10),
                  run_time=2.1, rate_func=linear)
        self.at("bottom corner")
        self.play(g.top[3].animate.set_color(CHANCE).set_opacity(1).scale(1.25),
                  g.side[3].animate.set_color(CHANCE).set_opacity(1).scale(1.25), run_time=0.8)
        pulse(highlight, base=5, amp=2, speed=2)
        self.finish()


class S11Samples(FilmScene):
    def construct(self):
        probs = np.array([9,3,3,1],dtype=float)/16
        labels = ["round yellow","round green","wrinkled yellow","wrinkled green"]
        base_x = [-4.5,-1.5,1.5,4.5]
        axes = VGroup(Line([-5.8,-1.95,0],[5.8,-1.95,0],color=GREY),
                      Line([-5.8,-1.95,0],[-5.8,2.6,0],color=GREY))
        self.play(Create(axes), run_time=0.6)
        bars = VGroup(*[Rectangle(width=1.5,height=0.15,color=GRID,fill_color=GRID,fill_opacity=0.7).move_to([x,-1.87,0]) for x in base_x])
        labs = VGroup(*[fit_text(s,2.7,24,TEAL,max_lines=1).move_to([x,-2.55,0]) for x,s in zip(base_x,labels)])
        self.play(FadeIn(bars), FadeIn(labs), run_time=0.7)
        self.at("Random offspring")
        small = np.array([6,2,5,3])/16
        self.play(*[bars[i].animate.stretch_to_fit_height(4.6*small[i]).move_to([base_x[i],-1.95+2.3*small[i],0]) for i in range(4)], run_time=1.6)
        self.at("Larger samples")
        expected = VGroup(*[DashedLine([x-0.9,-1.95+4.6*p,0],[x+0.9,-1.95+4.6*p,0],color=CHANCE) for x,p in zip(base_x,probs)])
        self.play(FadeIn(expected), *[bars[i].animate.stretch_to_fit_height(4.6*probs[i]).move_to([base_x[i],-1.95+2.3*probs[i],0]) for i in range(4)], run_time=2.4)
        computed = T("computed sampling", 24, TEAL).move_to([4.9, 3.25, 0])
        self.add(computed)
        self.finish()


class S12Mendel(FilmScene):
    def construct(self):
        obs, exp = [315,108,101,32], [313,104,104,35]
        names = ["round yellow","round green","wrinkled yellow","wrinkled green"]
        L = Ledger([(n,str(o),c) for n,o,c in zip(names,obs,[CHANCE,GREEN,PURPLE,WHITE])],
                   top_left=(-5.7,2.25),title="Mendel's observed pea counts",key_w=3.4,width=8.2,row_h=0.8,size=28)
        self.play(FadeIn(L), run_time=0.6)
        for i in range(4): self.play(L.reveal(i),run_time=0.35)
        self.at("not exactly")
        expected = VGroup(*[M(f"expected  {n}",27,TEAL).move_to([4.35,1.35-i*0.8,0]) for i,n in enumerate(exp)])
        self.play(LaggedStart(*[FadeIn(x,shift=LEFT*0.15) for x in expected],lag_ratio=0.12),run_time=1.2)
        self.at("repeated chance")
        marks = VGroup(*[Line([2.65,1.35-i*0.8,0],[2.9,1.35-i*0.8,0],color=CHANCE,stroke_width=5) for i in range(4)])
        self.play(LaggedStart(*[Create(x) for x in marks],lag_ratio=0.12),run_time=0.8)
        self.finish()


class S13Scope(FilmScene):
    def construct(self):
        g = punnett_grid(show_genotypes=False, show_seeds=True).scale(0.72).move_to([-2.5,-0.1,0])
        g.remove(g.top, g.side)
        boundary = SurroundingRectangle(g,color=GRID,buff=0.28,stroke_width=4)
        tag = T("this model",30,GRID,weight=BOLD).next_to(boundary,UP,buff=0.12)
        self.play(FadeIn(g),Create(boundary),FadeIn(tag),run_time=1.0)
        conditions = VGroup(chip("independent assortment",PURPLE,26),chip("complete dominance",PURPLE,26)).arrange(DOWN,buff=0.25).move_to([3.85,1.6,0])
        self.play(FadeIn(conditions),run_time=0.8)
        self.at("Linked genes")
        linked = VGroup(allele("R",0.55),Line(ORIGIN,RIGHT*0.7,color=TEAL,stroke_width=6),allele("Y",0.55)).arrange(RIGHT,buff=0.1).move_to([3.8,-0.2,0])
        other = T("linked: travel together",27,TEAL).next_to(linked,DOWN,buff=0.18)
        self.play(FadeIn(linked),FadeIn(other),run_time=0.8)
        self.at("Other allele")
        mid = seed("round","green",0.9).move_to([3.8,-2.15,0]); mid[0].set_fill(CHANCE,0.45)
        midlab = T("other relationships",27,TEAL).next_to(mid,DOWN,buff=0.12)
        self.play(FadeIn(mid),FadeIn(midlab),run_time=0.7)
        bob(mid,amp=0.05)
        self.finish()


class S14Rule(FilmScene):
    def construct(self):
        two = mini_grid(2,center=[-3.4,0.65,0],size=3.2)
        four = mini_grid(4,center=[3.1,0.65,0],size=4.2)
        h1 = T("one gene",32,TEAL,weight=BOLD).next_to(two,UP,buff=0.22)
        h2 = T("two genes",32,TEAL,weight=BOLD).next_to(four,UP,buff=0.22)
        self.play(Create(two),FadeIn(h1),Create(four),FadeIn(h2),run_time=1.5)
        steps = VGroup(chip("separate",PURPLE,28),chip("combine",CHANCE,28),chip("organize",GRID,28)).arrange(RIGHT,buff=0.5).move_to([0,-2.95,0])
        arrows = VGroup(Arrow(steps[0].get_right(),steps[1].get_left(),buff=0.08,color=GREY),Arrow(steps[1].get_right(),steps[2].get_left(),buff=0.08,color=GREY))
        self.at("Alleles separate")
        self.play(FadeIn(steps[0]),run_time=0.5)
        self.at("sex cells combine")
        self.play(GrowArrow(arrows[0]),FadeIn(steps[1]),run_time=0.6)
        self.at("square organizes")
        self.play(GrowArrow(arrows[1]),FadeIn(steps[2]),run_time=0.6)
        self.at("Two independent genes")
        counts = VGroup(M("2 types → 4 chances",28,TEXT).move_to([-3.4,-1.9,0]),
                        M("4 types → 16 chances",28,CHANCE).move_to([3.1,-1.9,0]))
        self.play(FadeIn(counts),run_time=0.8)
        pulse(four,base=3,amp=1,speed=2)
        self.finish()


class S15End(EndCard):
    LINE = "Genes that sort independently turn four sex-cell types into 9:3:3:1 chances."
