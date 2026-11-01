"""Hidden hearing loss: a normal threshold does not count synapses  (Biochemistrypedia explainer)

Timed to the SPOKEN words: every self.at("...") cue waits for that phrase in audio/words.json.

COLOR MAP (one color per concept, whole video)
  BLUE   = inner hair cell, ribbon and its vesicle pool (the synapse count)
  GREEN  = auditory nerve fibre and its terminal
  RED    = lost / missing / not equal / crossed out
  YELLOW = threshold (the test, in dB)
  TEAL   = proxy measures (SP/AP, ABR, EFR)
  ORANGE = noise exposure
  PURPLE = transmitter, and the complaint
  GOLD   = the bound (37 dB or more)
  GREY   = axes, outlines, de-emphasized
  TEXT   = neutral labels
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

PURPLE = "#B58CD9"
ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dashed_arr(a, b, color=GREY, w=4):
    a, b = np.array(a, float), np.array(b, float)
    d = (b - a) / np.linalg.norm(b - a)
    body = DashedLine(a, b - d * 0.2, color=color, stroke_width=w, dash_length=0.15)
    tip = Triangle(color=color, fill_opacity=1, stroke_width=0).scale(0.13)
    tip.rotate(np.arctan2(d[1], d[0]) - PI / 2).move_to(b - d * 0.1)
    return VGroup(body, tip)


def unit(cx, cy, s=1.0):
    """One sketch ribbon synapse: ribbon + a few vesicles above a nerve terminal."""
    rib = RoundedRectangle(corner_radius=0.05, width=0.16 * s, height=0.5 * s, stroke_color=BLUE,
                           stroke_width=3, fill_color=BLUE, fill_opacity=0.9).move_to([cx, cy + 0.22 * s, 0])
    ves = VGroup(*[Circle(radius=0.055 * s, stroke_width=0, fill_color=BLUE, fill_opacity=0.7)
                   .move_to([cx + dx * s, cy + dy * s, 0])
                   for dx, dy in [(-0.2, 0.32), (0.2, 0.32), (-0.2, 0.1), (0.2, 0.1)]])
    term = RoundedRectangle(corner_radius=0.12 * s, width=0.72 * s, height=0.34 * s, stroke_color=GREEN,
                            stroke_width=3, fill_color=GREEN, fill_opacity=0.35).move_to([cx, cy - 0.32 * s, 0])
    ghost = DashedVMobject(RoundedRectangle(corner_radius=0.12 * s, width=0.72 * s, height=0.34 * s,
                                            stroke_color=RED, stroke_width=3).move_to(term), num_dashes=18)
    ghost.set_color(RED)
    g = VGroup(rib, ves, term)
    g.rib, g.ves, g.term, g.ghost = rib, ves, term, ghost
    return g


def lose(u):
    return [FadeOut(u.rib), FadeOut(u.ves), ReplacementTransform(u.term, u.ghost)]


def level_axis(x, y0, y1):
    ax = Arrow([x, y0, 0], [x, y1, 0], buff=0, color=GREY, stroke_width=3, tip_length=0.2)
    up = T("louder", 22, GREY).next_to(ax.get_end(), RIGHT, buff=0.12)
    dn = T("quieter", 22, GREY).next_to(ax.get_start(), RIGHT, buff=0.12)
    return VGroup(ax, up, dn)


def dots(n_rows, n_cols, r=0.09, gap=0.27, color=TEXT):
    return VGroup(*[Circle(radius=r, stroke_width=0, fill_color=color, fill_opacity=0.9)
                    .move_to([c * gap, -rw * gap, 0]) for rw in range(n_rows) for c in range(n_cols)]).center()


class S00Title(TitleCard):
    LESSON = "Hidden hearing loss, gene therapy and regeneration"
    TITLE = "A normal threshold counts nothing"


def heading(text, color=TEXT):
    return T(text, 32, color, font=TITLE_FONT).move_to([0, 3.1, 0])


def clear(scene):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.5)


class S01Normal(SpokenScene):
    def construct(self):
        head = heading("A normal threshold can hide damage")
        test = T("Hearing threshold", 28, YELLOW).move_to([-3.5, 2, 0])
        axis = level_axis(-5.7, -1.5, 1.2)
        baseline = DashedLine([-4.6, -0.6, 0], [-1.3, -0.6, 0], color=GREY)
        marker = Line([-4.6, -0.6, 0], [-1.3, -0.6, 0], color=YELLOW, stroke_width=7)
        units = VGroup(*[unit(2.0 + dx, y, 1.5) for y in (0.8, -0.9) for dx in (0, 2.5)])
        sketch = T("Illustrative synapse sketch", 24, BLUE).move_to([3.2, 2, 0])
        self.at("A normal hearing test")
        self.play(FadeIn(head), FadeIn(test), Create(axis), Create(baseline), Create(marker), FadeIn(units), FadeIn(sketch), run_time=0.8)
        self.at("In mice")
        mouse = T("Mice after loud noise", 24, ORANGE).move_to([0, -2.5, 0])
        self.play(FadeIn(mouse), marker.animate.shift(UP * 1.2), run_time=0.6)
        self.at("recovered after loud noise")
        self.play(marker.animate.shift(DOWN * 1.2), run_time=0.8)
        self.at("Yet about half")
        ghosts = VGroup(*[VGroup(DashedVMobject(units[i].rib.copy().set_fill(opacity=0), num_dashes=12).set_color(BLUE), DashedVMobject(units[i].term.copy().set_fill(opacity=0), num_dashes=16).set_color(GREEN)) for i in (1, 2)])
        self.play(*[FadeOut(units[i]) for i in (1, 2)], FadeIn(ghosts), run_time=0.8)
        self.at("were lost at one place")
        lost = T("About half lost at one cochlear place", 24, RED).move_to([0, -3.2, 0])
        self.play(FadeIn(lost), run_time=0.5)
        self.at("quietest sound")
        self.play(Indicate(marker, color=YELLOW), run_time=0.7)
        self.at("does not count")
        self.play(Indicate(VGroup(units[0], units[3]), color=BLUE), run_time=0.7)
        self.at("recovered sensitivity can conceal injury")
        self.play(Indicate(head, color=RED, scale_factor=1.03), run_time=0.8)
        self.at("Repair then poses different problems")
        clear(self)
        root = heading("Two repair problems")
        self.play(FadeIn(root), run_time=0.4)
        a = chip("Restore release", BLUE, 32).move_to([-3.2, 0.5, 0])
        al = T("in surviving cells", 26, BLUE).move_to([-3.2, -0.5, 0])
        b = chip("Replace hair cells", BLUE, 32).move_to([3.2, 0.5, 0])
        bl = T("where cells are lost", 26, RED).move_to([3.2, -0.5, 0])
        self.at("restoring release")
        self.play(GrowArrow(arr([-0.5, 2.4, 0], [-3.2, 1.2, 0])), FadeIn(a), FadeIn(al), run_time=0.6)
        self.at("or replacing hair cells")
        self.play(GrowArrow(arr([0.5, 2.4, 0], [3.2, 1.2, 0])), FadeIn(b), FadeIn(bl), run_time=0.6)
        self.finish()


class S03Noise(SpokenScene):
    def construct(self):
        context = heading("Male CBA/CaJ mice · Kujawa & Liberman")
        self.at("Kujawa and Liberman")
        self.play(FadeIn(context), run_time=0.6)
        xs = [-3.8, 0, 3.8]
        timeline = Line([-5.8, 1.9, 0], [5.8, 1.9, 0], color=GREY)
        heads = VGroup(*[T(t, 28).move_to([x, 2.35, 0]) for x, t in zip(xs, ("Control", "2 weeks", "8 weeks"))])
        threshold = VGroup(*[Line([x-0.9, 0.8, 0], [x+0.9, 0.8, 0], color=YELLOW, stroke_width=7) for x in xs[:2]])
        bars = VGroup(*[Rectangle(width=1.1, height=h, stroke_color=BLUE, fill_color=BLUE, fill_opacity=0.5).move_to([x, -2.4+h/2, 0]) for x,h in ((xs[0],1.8),(xs[2],0.9))])
        self.at("By two weeks")
        self.play(Create(timeline), FadeIn(heads[:2]), Create(threshold), run_time=0.8)
        thrlabel = T("Threshold back to old value", 25, YELLOW).move_to([-1.9, 0.1, 0])
        self.play(FadeIn(thrlabel), run_time=0.5)
        self.at("Hair cells remained intact")
        intact = T("Hair cells\nintact", 26, BLUE).move_to([0, -1.6, 0])
        self.play(FadeIn(intact), run_time=0.5)
        self.at("At eight weeks")
        label = T("Ribbon count · 32 kHz place", 26, BLUE).move_to([0,-3.1,0])
        self.play(FadeIn(heads[2]), FadeIn(label), GrowFromEdge(bars[0],DOWN), GrowFromEdge(bars[1],DOWN), run_time=0.8)
        self.at("about half of control")
        half = T("≈ half", 26, BLUE).move_to([3.8, -0.7, 0])
        self.play(FadeIn(half), run_time=0.5)
        self.at("The cochlear nerve degenerated later")
        clear(self)
        self.play(FadeIn(heading("Nerve degeneration came later", GREEN)), run_time=0.4)
        start = chip("8-week ribbon count", BLUE, 28).move_to([-3.1,0,0])
        later = chip("Later nerve degeneration", GREEN, 28).move_to([3.1,0,0])
        self.play(FadeIn(start), GrowArrow(arr([-0.7,0,0],[0.5,0,0],GREEN)), FadeIn(later), run_time=0.8)
        self.finish()


class S04People(SpokenScene):
    def construct(self):
        self.at("Human temporal bones")
        post = chip("Human temporal bones", TEXT, 30).move_to([-3.4,2.4,0])
        counted = T("Postmortem nerve-fibre counts", 25, GREEN).move_to([-3.4,0.9,0])
        result = T("Fibre loss\nworse with noise", 28, GREEN).move_to([-3.4,-0.7,0])
        self.play(FadeIn(post), FadeIn(counted), GrowArrow(arr([-3.4,0.5,0],[-3.4,-0.1,0],GREEN)), FadeIn(result), run_time=1)
        self.at("But no one can count synapses")
        living = T("Living ear", 30, TEXT).move_to([3.3,2.4,0])
        box = DashedVMobject(RoundedRectangle(width=3.6,height=1.6,corner_radius=0.2),num_dashes=30).set_color(BLUE).move_to([3.3,-0.7,0])
        question = T("Synapse count: ?", 28, BLUE).move_to(box)
        self.play(FadeIn(living), Create(box), FadeIn(question), run_time=0.7)
        self.at("Physiological proxies")
        proxy = chip("Physiological proxies", TEAL, 26).move_to([3.3,1.2,0])
        arrow = dashed_arr([3.3,0.75,0],[3.3,0.2,0],TEAL)
        uncertain = T("Uncertain sensitivity", 24, TEAL).move_to([3.3,-2,0])
        self.play(FadeIn(proxy), Create(arrow), FadeIn(uncertain), run_time=0.8)
        self.at("A listening complaint alone")
        clear(self)
        row = VGroup(chip("Listening complaint",PURPLE,30),T("≠",50,RED),chip("Established lesion",BLUE,30)).arrange(RIGHT,buff=0.4)
        self.play(FadeIn(row), run_time=0.8)
        self.finish()


class S05Therapy(SpokenScene):
    def construct(self):
        self.at("Gene replacement has improved hearing")
        intro = heading("Gene replacement: hearing improved")
        genotype = chip("Children with OTOF-related deafness", TEXT, 28).move_to([0,1.7,0])
        self.play(FadeIn(intro), FadeIn(genotype), run_time=0.8)
        cell = RoundedRectangle(width=6,height=2.8,corner_radius=0.5,stroke_color=BLUE,fill_color=BLUE,fill_opacity=0.16).move_to([0,-0.5,0])
        clab = T("Surviving inner hair cell",28,BLUE).move_to([0,-1.2,0])
        self.at("cells that survive")
        self.play(FadeIn(cell),FadeIn(clab),run_time=0.7)
        self.at("too large for one conventional")
        clear(self)
        head = heading("Otoferlin gene: too large for one AAV")
        full = chip("Full-length otoferlin gene",BLUE,28).move_to([-1.5,1.3,0])
        vector = RoundedRectangle(width=2,height=1,corner_radius=0.2,stroke_color=GREY).move_to([4,1.3,0])
        vl = T("One AAV",24,GREY).next_to(vector,DOWN,buff=0.2)
        self.play(FadeIn(head),FadeIn(full),Create(vector),FadeIn(vl),run_time=0.8)
        self.at("In mice")
        clear(self)
        self.play(FadeIn(heading("Mouse evidence · dual AAV")), run_time=0.4)
        cell.move_to([0,-0.6,0]); clab.move_to([0,-1.4,0])
        p1 = chip("Gene portion 1",BLUE,26).move_to([-3.4,1.8,0])
        p2 = chip("Gene portion 2",BLUE,26).move_to([3.4,1.8,0])
        self.at("split it across two vectors")
        self.play(FadeIn(p1),FadeIn(p2),FadeIn(cell),FadeIn(clab),run_time=0.7)
        self.at("cells receiving both")
        self.play(p1.animate.move_to([-1.6,-0.2,0]),p2.animate.move_to([1.6,-0.2,0]),run_time=0.9)
        self.at("could rebuild it")
        rebuilt = chip("Full-length otoferlin",BLUE,28).move_to([0,-0.2,0])
        self.play(ReplacementTransform(VGroup(p1,p2),rebuilt),run_time=0.8)
        self.at("Human trials test hearing recovery separately")
        clear(self)
        self.play(FadeIn(heading("Human trial · DB-OTO")),FadeIn(T("OTOF-related deafness",28,TEXT).move_to([0,2.2,0])),run_time=0.7)
        self.at("nine of 12 children")
        nine = T("9 / 12 children",44,YELLOW).move_to([0,0.9,0])
        self.play(FadeIn(nine),run_time=0.5)
        self.at("week 24 endpoint")
        week = T("Week 24 endpoint",28,TEXT).move_to([0,0,0])
        self.play(FadeIn(week),run_time=0.4)
        self.at("an average threshold")
        endpoint = T("Average threshold ≤ 70 dB HL",30,YELLOW).move_to([0,-0.9,0])
        self.play(FadeIn(endpoint),run_time=0.5)
        self.at("Three reached average normal sensitivity")
        normal = T("3 / 12: average normal sensitivity",28,YELLOW).move_to([0,-1.9,0])
        self.play(FadeIn(normal),run_time=0.6)
        self.at("This treats")
        self.play(Indicate(self.mobjects[1],scale_factor=1.05),run_time=0.5)
        self.at("Lifelong benefit remains unproven")
        self.play(FadeIn(T("Lifelong benefit remains unproven",26,RED).move_to([0,-3,0])),run_time=0.6)
        self.finish()


class S06Regeneration(SpokenScene):
    def construct(self):
        def row(name,y):
            label = T(name,27,TEXT).move_to([-3.5,y,0])
            cells = VGroup(*[RoundedRectangle(width=0.55,height=0.9,corner_radius=0.12,stroke_color=BLUE,fill_color=BLUE,fill_opacity=0.25).move_to([1.5+i*1.25,y,0]) for i in range(3)])
            ghost = DashedVMobject(cells[1].copy().set_fill(opacity=0),num_dashes=14).set_color(RED)
            return label,cells,ghost
        self.at("Birds show")
        self.play(FadeIn(heading("Hair-cell replacement depends on the organ")),run_time=0.5)
        bird,bc,bg=row("Birds · auditory organ",1.5)
        self.play(FadeIn(bird),FadeIn(VGroup(bc[0],bc[2],bg)),run_time=0.6)
        self.at("They regrow auditory hair cells")
        self.play(ReplacementTransform(bg,bc[1]),run_time=0.9)
        self.at("Fish regrow hair cells")
        fish,fc,fg=row("Fish · lateral line",0)
        self.play(FadeIn(fish),FadeIn(VGroup(fc[0],fc[2],fg)),run_time=0.5)
        self.play(ReplacementTransform(fg,fc[1]),run_time=0.9)
        self.at("Mature mammalian cochleas")
        mammal,mc,mg=row("Mature mammal · cochlea",-1.5)
        self.play(FadeIn(mammal),FadeIn(VGroup(mc[0],mc[2],mg)),run_time=0.7)
        self.at("lack comparable spontaneous replacement")
        self.play(FadeIn(T("No comparable spontaneous replacement",24,RED).move_to([0,-2.7,0])),run_time=0.6)
        self.at("Mammals do have a vestibular exception")
        clear(self)
        head=heading("Guinea-pig utricle · vestibular")
        self.play(FadeIn(head),run_time=0.5)
        lab,cells,ghost=row("After damage",0.8)
        self.play(FadeIn(lab),FadeIn(VGroup(cells[0],cells[2],ghost)),run_time=0.5)
        self.at("Hair cells reappeared")
        self.play(ReplacementTransform(ghost,cells[1]),run_time=0.8)
        self.at("That is a different organ")
        self.play(FadeIn(T("Vestibular organ ≠ cochlea",32,TEXT).move_to([0,-1.2,0])),run_time=0.7)
        self.at("Replacing lost cochlear hair cells")
        clear(self)
        self.play(FadeIn(heading("Replace lost cochlear hair cells")),run_time=0.5)
        target=DashedVMobject(RoundedRectangle(width=6.5,height=2,corner_radius=0.3),num_dashes=40).set_color(BLUE)
        self.play(Create(target),FadeIn(T("Experimental repair goal",32,BLUE)),run_time=0.8)
        self.finish()


class S02Ribbon(SpokenScene):
    def construct(self):
        self.at("What must a repaired synapse do")
        head=heading("What must a repaired synapse do?")
        self.play(FadeIn(head),run_time=0.6)
        cx=-3.3
        cell=RoundedRectangle(corner_radius=0.5,width=5,height=2,stroke_color=BLUE,stroke_width=4,fill_color=BLUE,fill_opacity=0.16).move_to([cx,1.5,0])
        clab=T("Inner hair cell",30,BLUE).move_to([cx,1.8,0])
        self.at("An inner hair cell")
        self.play(FadeIn(cell),FadeIn(clab),run_time=0.6)
        term=RoundedRectangle(corner_radius=0.3,width=3.6,height=0.9,stroke_color=GREEN,stroke_width=4,fill_color=GREEN,fill_opacity=0.3).move_to([cx,-1.1,0])
        fibre=Line([cx,-1.5,0],[cx,-2.7,0],color=GREEN,stroke_width=8)
        flab=T("Auditory nerve fibre",25,GREEN).move_to([cx,-3.15,0])
        drops=VGroup(*[Dot([cx+dx,0.5,0],radius=0.1,color=PURPLE) for dx in (-0.6,0,0.6)])
        self.at("releases transmitter")
        self.play(FadeIn(term),Create(fibre),FadeIn(flab),FadeIn(drops),run_time=0.4)
        self.play(drops.animate.shift(DOWN*1.1).set_opacity(0),run_time=0.8)
        rib=RoundedRectangle(corner_radius=0.08,width=0.3,height=0.9,stroke_color=BLUE,fill_color=BLUE,fill_opacity=0.95).move_to([cx,0.45,0])
        ves=VGroup(*[Dot([cx+dx,y,0],radius=0.1,color=BLUE) for dx,y in ((-0.5,0.7),(0.5,0.7),(-0.6,0.2),(0.6,0.2))])
        rlab=T("Ribbon + vesicle pool",24,BLUE).move_to([cx,2.75,0])
        self.at("Its ribbon helps keep vesicles in supply")
        self.play(FadeOut(head),FadeIn(rib),FadeIn(ves),FadeIn(rlab),run_time=0.8)
        self.at("is essential for release")
        essential=T("Otoferlin\nessential for release",28,BLUE).move_to([3.1,2.5,0])
        self.play(FadeIn(essential),run_time=0.5)
        self.at("In mice lacking it")
        absent=VGroup(T("Mouse evidence 1",24,GREY),T("Otoferlin absent",27,RED),T("Release almost abolished",26,PURPLE)).arrange(DOWN,buff=0.2).move_to([3.1,0.7,0])
        self.play(FadeIn(absent),run_time=0.7)
        self.at("Changing its calcium binding")
        altered=VGroup(T("Mouse 2 · otoferlin present",24,GREY),T("Calcium binding altered",26,BLUE),T("Release calcium sensitivity ↓",25,PURPLE)).arrange(DOWN,buff=0.2).move_to([3.1,-1.3,0])
        self.play(FadeIn(altered),run_time=0.7)
        self.at("That supports")
        self.play(FadeIn(T("Supports a calcium-sensing role",26,TEXT).move_to([2.7,-2.8,0])),run_time=0.5)
        self.at("without showing it is the only sensor")
        self.play(FadeIn(T("Does not establish the only sensor",22,GREY).move_to([2.7,-3.4,0])),run_time=0.5)
        self.finish()


class S07End(EndCard):
    LINE = "Ask what a number counts, and what it leaves out."
