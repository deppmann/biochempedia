"""Water, salt and nitrogenous waste: schematic, word-synced animation.

COLOR MAP (preserved from the original film)
  BLUE   = water / seawater
  YELLOW = salt (sodium chloride; other inorganic ions labelled explicitly)
  ORANGE = the kidney route (kidneys, urine)
  GREEN  = the nasal salt gland route (glands, nasal fluid)
  RED    = the problem / toxicity
  GREY   = outlines, axes, de-emphasized
  TEAL   = organic solutes / nitrogen waste
"""
import numpy as np
from bp_style import *

ORANGE = "#F29E4C"


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.06, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def box(w, h, color, x, y, op=0.2, sw=3):
    return RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=color, stroke_width=sw,
                            fill_color=color, fill_opacity=op).move_to([x, y, 0])


def lines(txt, size=24, color=GREY, **kw):
    return VGroup(*[T(s, size, color, **kw) for s in txt.split("\n")]).arrange(DOWN, buff=0.08)


def bird(cx, cy, w, h, label="cormorant"):
    b = box(w, h, GREY, cx, cy, op=0.08, sw=3)
    l = T(label, 24, GREY).next_to(b, UP, buff=0.12)
    return VGroup(b, l)


def vial(x, y, color, w=0.8, h=1.1):
    return box(w, h, color, x, y, op=0.3, sw=3)


def heading(txt):
    return T(txt, 32, TEXT, font=TITLE_FONT).move_to([0, 3.15, 0])


def flow(txt, start, end, color, label_pos, size=26, w=5):
    return VGroup(arr(start, end, color, w=w), lines(txt, size, color).move_to(label_pos))


def clear(scene):
    scene.play(*[FadeOut(m) for m in list(scene.mobjects)], run_time=0.4)


def travel(scene, start, end, color, duration=0.6):
    d = Dot(start, radius=0.10, color=color)
    scene.add(d)
    scene.play(d.animate.move_to(end), run_time=duration)
    scene.remove(d)


class S00Title(TitleCard):
    LESSON = "Osmoregulation and nitrogenous waste"
    TITLE = "Water, Salt and Nitrogenous Waste"

    def construct(self):
        title = T(self.TITLE, 44, TEXT, font=TITLE_FONT).move_to([0, 1.1, 0])
        habitats = VGroup(*[VGroup(box(3.4, 1.2, c, x, -0.8), T(t, 28, c).move_to([x, -0.8, 0]))
                              for x, t, c in [(-4.3, "sea", BLUE), (0, "fresh water", BLUE), (4.3, "land", GREY)]])
        self.play(FadeIn(title), run_time=0.5)
        self.play(FadeIn(habitats), run_time=0.5)
        self.finish()


class S01Sea(SpokenScene):
    def construct(self):
        h = heading("A shared water and salt budget")
        body = bird(0, 0, 3.4, 2.6, "animal")
        water = flow("water", [-5, 0.6, 0], [-1.8, 0.6, 0], BLUE, [-3.5, 1.2, 0])
        salt = flow("salt", [1.8, -0.6, 0], [5, -0.6, 0], YELLOW, [3.5, -1.25, 0])
        self.at("Every animal")
        self.play(FadeIn(h), FadeIn(body), FadeIn(water), FadeIn(salt), run_time=0.7)
        self.at("gains and losses")
        self.play(Indicate(water, color=BLUE), Indicate(salt, color=YELLOW), run_time=0.7)
        self.at("surroundings keep pulling")
        self.play(water.animate.shift(RIGHT * 0.3), salt.animate.shift(RIGHT * 0.3), run_time=0.7)
        self.at("A marine bony fish")
        marine = bird(0, 0, 3.4, 2.6, "marine bony fish")
        wo = flow("water lost", [1.8, 0.6, 0], [5.4, 0.6, 0], BLUE, [3.7, 1.25, 0])
        si = flow("salt gained", [-5.4, -0.6, 0], [-1.8, -0.6, 0], YELLOW, [-3.7, -1.25, 0])
        self.play(ReplacementTransform(body, marine), ReplacementTransform(water, wo), ReplacementTransform(salt, si), run_time=0.6)
        self.at("In freshwater")
        fresh = bird(0, 0, 3.4, 2.6, "freshwater bony fish")
        wi = flow("water enters", [5.4, 0.6, 0], [1.8, 0.6, 0], BLUE, [3.7, 1.25, 0])
        so = flow("salts leak out", [-1.8, -0.6, 0], [-5.4, -0.6, 0], YELLOW, [-3.7, -1.25, 0])
        self.play(ReplacementTransform(marine, fresh), ReplacementTransform(wo, wi), ReplacementTransform(si, so), run_time=0.7)
        self.at("On land")
        land = bird(0, 0, 3.4, 2.6, "land animal")
        evap = flow("evaporation", [1.8, 0.6, 0], [5.4, 1.7, 0], BLUE, [3.6, 2.3, 0])
        self.play(ReplacementTransform(fresh, land), ReplacementTransform(wi, evap), FadeOut(so), run_time=0.7)
        self.at("Even marine invertebrates")
        clear(self)
        cell = VGroup(Circle(radius=1.5, color=GREY), T("cell", 26).move_to([0, -1.0, 0]))
        hh = heading("Marine invertebrate: stable cell volume")
        ext = lines("external concentration\nchanges", 26, BLUE).move_to([-4.3, 0.6, 0])
        self.play(FadeIn(hh), Create(cell), FadeIn(ext), run_time=0.6)
        self.at("adjust organic molecules")
        osm = chip("organic osmolytes", TEAL, 22).move_to([0, 0.35, 0])
        note = lines("adjust solutes\ninside the cell", 26, TEAL).move_to([4.3, 0.4, 0])
        self.play(FadeIn(osm), FadeIn(note), run_time=0.6)
        level = box(1.1, 0.16, TEAL, 0, -0.25, op=0.6)
        self.play(FadeIn(level), run_time=0.2)
        self.play(level.animate.stretch_to_fit_width(2.1), ext.animate.set_opacity(0.6), run_time=0.7)
        self.at("keeps the cells")
        self.play(Indicate(cell[0], color=TEAL, scale_factor=1.0), Indicate(osm, color=TEAL), run_time=0.6)
        self.at("Nitrogen disposal")
        clear(self)
        n = chip("nitrogen waste", TEAL, 30).move_to([-3.5, 0, 0])
        loss = flow("water used in disposal", [-1.6, 0, 0], [4.8, 0, 0], BLUE, [2, 0.8, 0])
        self.play(FadeIn(n), FadeIn(loss), run_time=0.7)
        self.finish()


class S02Kidney(SpokenScene):
    def construct(self):
        h = heading("Marine bony fish")
        gut = chip("intestine", GREY, 28).move_to([-1.0, 1.35, 0])
        drink = flow("seawater", [-5.7, 1.35, 0], [-2.5, 1.35, 0], BLUE, [-4.2, 2.0, 0])
        self.at("Marine bony fish")
        self.play(FadeIn(h), FadeIn(gut), FadeIn(drink), run_time=0.7)
        absorb = flow("water + ions absorbed", [0.3, 1.35, 0], [5.5, 1.35, 0], BLUE, [3.1, 2.0, 0])
        self.at("intestine absorbs")
        self.play(FadeIn(absorb), run_time=0.7)
        gill = chip("gills", GREY, 28).move_to([-1, -0.3, 0])
        out = flow("mostly sodium + chloride", [0, -0.3, 0], [5.5, -0.3, 0], YELLOW, [3.1, 0.25, 0])
        self.at("Excess sodium and chloride")
        self.play(FadeIn(gill), FadeIn(out), run_time=0.7)
        kidney = chip("kidneys", ORANGE, 28).move_to([-1, -2.0, 0])
        urine = flow("absorbed magnesium + sulfate\nsmall urine volume", [0.3, -2, 0], [5.5, -2, 0], ORANGE, [3.2, -2.9, 0], size=23, w=3)
        self.at("Absorbed magnesium")
        self.play(FadeIn(kidney), FadeIn(urine), run_time=0.7)
        self.at("Freshwater bony fish")
        clear(self)
        h = heading("Freshwater bony fish")
        gill = chip("gills", GREY, 28).move_to([0, 0.7, 0])
        leak = VGroup(flow("water enters", [-5.8, 0.7, 0], [-1, 0.7, 0], BLUE, [-3.5, 1.3, 0]),
                      flow("salt leaks out", [1, 0.7, 0], [5.8, 0.7, 0], YELLOW, [3.5, 1.3, 0]))
        self.play(FadeIn(h), FadeIn(gill), FadeIn(leak), run_time=0.7)
        self.at("kidneys make plenty")
        kidney = chip("kidneys", ORANGE, 28).move_to([-3.5, -1.5, 0])
        urine = flow("large dilute urine stream", [-2.2, -1.5, 0], [5.6, -1.5, 0], ORANGE, [1.8, -2.2, 0], w=10)
        self.play(FadeIn(kidney), FadeIn(urine), run_time=0.7)
        self.at("gills actively take up")
        active = flow("active sodium + chloride uptake · ATP", [5.8, 0.7, 0], [1, 0.7, 0], YELLOW, [2.8, 1.9, 0], size=23)
        self.play(FadeOut(leak), FadeIn(active), run_time=0.7)
        self.at("In salmon and eels")
        clear(self)
        h = heading("Salmon and eels: gill cells switch")
        g = chip("gill cells", GREY, 30).move_to([0, 0, 0])
        uptake = flow("salt uptake", [-5.7, 0, 0], [-1.5, 0, 0], YELLOW, [-3.6, 0.8, 0])
        self.play(FadeIn(h), FadeIn(g), FadeIn(uptake), run_time=0.6)
        self.at("switch between salt uptake")
        secretion = flow("salt secretion", [1.5, 0, 0], [5.7, 0, 0], YELLOW, [3.6, 0.8, 0])
        self.play(ReplacementTransform(uptake, secretion), run_time=0.7)
        self.finish()


class S03Nitrogen(SpokenScene):
    def construct(self):
        h = heading("Nitrogen waste: three tradeoffs")
        protein = chip("protein breakdown", GREY, 28).move_to([-3.8, 1.8, 0])
        ammonia = chip("ammonia", TEAL, 28).move_to([2, 1.8, 0])
        a = arr([-1.6, 1.8, 0], [0.7, 1.8, 0], TEAL)
        self.at("Protein breakdown")
        self.play(FadeIn(h), FadeIn(protein), FadeIn(ammonia), GrowArrow(a), run_time=0.7)
        # One grouped row per waste keeps the qualitative table compact.
        heads = VGroup(*[T(t, 24, c).move_to([x, 1.4, 0]) for x,t,c in
                         [(-4.8,"waste",TEAL),(-2,"toxicity",RED),(0.8,"water needed",BLUE),(4.2,"synthesis cost",TEXT)]])
        def row(y, name, toxicity, water, cost):
            return VGroup(*[lines(t, 23, c).move_to([x,y,0]) for x,t,c in
                           [(-4.8,name,TEAL),(-2,toxicity,RED),(0.8,water,BLUE),(4.2,cost,TEXT)]])
        r1 = row(0.25,"ammonia","toxic","plenty","no ATP to form")
        r2 = row(-1.0,"urea","less toxic","less","ATP required")
        r3 = row(-2.25,"uric acid","—","very little","usually costlier")
        self.at("It needs no ATP")
        self.play(FadeOut(protein), FadeOut(ammonia), FadeOut(a), FadeIn(heads), FadeIn(r1), run_time=0.7)
        dissolved = lines("dissolved waste", 24, BLUE).move_to([0,-3.25,0])
        self.at("plenty of water")
        self.play(FadeIn(dissolved), run_time=0.5)
        self.at("Urea costs")
        self.play(FadeIn(r2[0]), FadeIn(r2[3]), run_time=0.6)
        self.at("It is less toxic")
        self.play(FadeIn(r2[1]), FadeIn(r2[2]), run_time=0.6)
        self.at("Uric acid leaves")
        self.play(FadeIn(r3[0]), FadeIn(r3[1]), FadeIn(r3[2]), run_time=0.6)
        paste = VGroup(box(1.1,0.35,TEAL,2.9,-3.15,op=0.7), T("paste / solid",23,TEAL).move_to([5.1,-3.15,0]))
        self.at("a paste or solid")
        self.play(dissolved.animate.move_to([-2,-3.15,0]), FadeIn(paste), run_time=0.5)
        self.at("It is usually")
        self.play(FadeIn(r3[3]), run_time=0.6)
        self.at("Each waste trades")
        self.play(Indicate(heads, color=TEXT, scale_factor=1.02), run_time=0.7)
        self.finish()


class S04Organs(SpokenScene):
    def construct(self):
        h = heading("Organs control what leaves")
        self.at("Organs control")
        self.play(FadeIn(h), run_time=0.5)
        tub = box(10.6,1.3,ORANGE,0,-0.2,op=0.12)
        name = T("tubule",26,ORANGE).move_to([4,-0.2,0])
        label = T("Most vertebrate kidneys",28,ORANGE).move_to([0,2.2,0])
        filt = flow("filtration\nat glomerulus",[-4,1.5,0],[-4,0.5,0],GREY,[-4,2.1,0],size=22)
        self.at("Most vertebrate kidneys")
        self.play(FadeIn(label), Create(tub), FadeIn(name), run_time=0.6)
        self.at("filter body fluid")
        self.play(FadeIn(filt), run_time=0.5)
        reabs = flow("reabsorption\nuseful substances",[-0.7,-0.1,0],[-0.7,-2.1,0],BLUE,[-2,-2.7,0],size=23)
        self.at("reabsorb useful substances")
        self.play(FadeIn(reabs), run_time=0.6)
        sec = flow("secretion\nother substances",[2,1.5,0],[2,0.5,0],TEAL,[3.6,1.6,0],size=23)
        self.at("secrete others")
        self.play(FadeIn(sec), run_time=0.6)
        self.at("Insect malpigian tubules")
        clear(self)
        label = heading("Insect Malpighian tubules: no filtration")
        tub = box(9.0,1.3,GREY,-0.8,-0.3,op=0.08)
        name = T("lumen",24,GREY).move_to([-4,-0.3,0])
        self.play(FadeIn(label), Create(tub), FadeIn(name), run_time=0.6)
        ions = flow("ion secretion",[-2,1.8,0],[-2,0.4,0],YELLOW,[-3.7,1.9,0])
        self.at("They secrete ions")
        self.play(FadeIn(ions), run_time=0.5)
        water = flow("water follows\nby osmosis",[0.3,1.8,0],[0.3,0.4,0],BLUE,[1.5,1.9,0],size=24)
        self.at("water follows")
        self.play(FadeIn(water), run_time=0.5)
        waste = flow("wastes",[-0.5,-2.4,0],[-0.5,-1,0],TEAL,[-2,-2.4,0])
        self.at("Wastes enter")
        self.play(FadeIn(waste), run_time=0.5)
        rect = chip("rectum",GREY,26).move_to([4.8,-0.3,0])
        recovery = flow("salts + water recovered",[4.8,-0.9,0],[4.8,-2.4,0],BLUE,[3,-3.0,0],size=24)
        self.at("The rectum")
        self.play(FadeOut(waste), FadeIn(rect), FadeIn(recovery), run_time=0.7)
        self.finish()


class S06Shark(SpokenScene):
    def construct(self):
        h = heading("Sharks retain urea for water balance")
        plasma = box(5.4,2.7,GREY,2.8,0.7,op=0.08)
        pl = T("shark plasma",27).move_to([2.8,2.4,0])
        urea = chip("retained urea",TEAL,26).move_to([2.8,0.7,0])
        self.at("Sharks retain urea")
        self.play(FadeIn(h), Create(plasma), FadeIn(pl), FadeIn(urea), run_time=0.7)
        ions = chip("inorganic ions",YELLOW,24).move_to([2.8,1.5,0])
        tmao = chip("TMAO",TEAL,24).move_to([2.8,-0.15,0])
        self.at("Urea and other dissolved particles")
        self.play(FadeIn(ions), FadeIn(tmao), run_time=0.6)
        total = lines("total osmolality:\nslightly above seawater",26,TEXT).move_to([-3.6,1.5,0])
        self.at("slightly above seawater")
        self.play(FadeIn(total), run_time=0.6)
        slow = flow("slow water entry",[-5.9,-0.4,0],[-0.1,-0.4,0],BLUE,[-3.6,0.3,0])
        self.at("water enters slowly")
        self.play(FadeIn(slow), run_time=0.6)
        self.at("Their kidneys recover")
        # Zoom into the two outgoing routes, preserving the plasma/urea position.
        self.play(FadeOut(total), FadeOut(slow), FadeOut(ions), FadeOut(tmao), run_time=0.3)
        kidney = chip("kidneys",ORANGE,26).move_to([-3.8,-0.8,0])
        ret = flow("most filtered urea returned",[-2.5,-0.8,0],[1.3,0.15,0],TEAL,[-0.4,-1.5,0],size=23)
        self.play(FadeIn(kidney), FadeIn(ret), run_time=0.6)
        self.at("They still regulate salts")
        self.play(Indicate(plasma, color=YELLOW, scale_factor=1.0), run_time=0.6)
        gland = chip("rectal gland",GREY,26).move_to([-3.8,-2.6,0])
        salt = flow("concentrated sodium chloride",[-2.3,-2.6,0],[5.7,-2.6,0],YELLOW,[1.9,-3.2,0],size=23)
        self.at("A rectal gland")
        self.play(FadeIn(gland), FadeIn(salt), run_time=0.7)
        self.finish()


class S05Water(SpokenScene):
    def construct(self):
        head = heading("A smaller example: seabird salt glands")
        gulp = box(2.4,2.6,BLUE,-5,0.2,op=0.3)
        gs = chip("salt",YELLOW,26).move_to(gulp)
        gl = lines("a gulp of\nseawater",24,BLUE).next_to(gulp,DOWN,buff=0.15)
        gland = chip("nasal salt gland",GREEN,24).move_to([-1.5,0.2,0])
        a1 = arr([-3.7,0.2,0],[-3.05,0.2,0],GREY)
        a2 = arr([-0.1,0.2,0],[0.7,0.2,0],GREY)
        out = box(2.4,1.5,GREEN,2,0.75,op=0.2)
        os_ = chip("same salt",YELLOW,24).move_to(out)
        kept = box(2.4,1.1,BLUE,2,-0.55,op=0.35)
        ol = lines("gland fluid:\nmore concentrated",22,GREEN).move_to([4.95,0.85,0])
        kl = lines("water the\nbird keeps",22,BLUE).move_to([4.95,-0.65,0])
        self.at("One smaller example")
        self.play(FadeIn(head), run_time=0.5)
        self.at("seabirds use nasal salt glands")
        self.play(FadeIn(gland), run_time=0.6)
        self.at("Salt secretion")
        self.play(FadeIn(out), FadeIn(os_), FadeIn(ol), run_time=0.6)
        self.at("a gulp of seawater's salt")
        self.play(FadeIn(VGroup(gulp,gs,gl)), run_time=0.6)
        self.at("in less water")
        self.play(GrowArrow(a1), GrowArrow(a2), run_time=0.6)
        self.at("They keep the difference")
        self.play(FadeIn(kept), FadeIn(kl), run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Animals balance water and salt against their surroundings."
    def construct(self):
        line = T(self.LINE,40,TEXT,font=TITLE_FONT).move_to([0,1.1,0])
        symbols = VGroup(chip("water",BLUE,28),chip("salt",YELLOW,28),chip("nitrogen waste",TEAL,28)).arrange(RIGHT,buff=0.65).move_to([0,-0.5,0])
        self.play(FadeIn(line),FadeIn(symbols),run_time=0.7)
        self.finish()
