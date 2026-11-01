"""Animal development: from one egg to organized tissues  (Biochemistrypedia explainer)

COLOR MAP (one color per concept, whole video)
  BLUE   = cells / cytoplasm (zygote and blastomeres)
  GREEN  = volume (conserved)
  TEAL   = membrane (surface area)
  ORANGE = nuclei
  GOLD   = yolk
  YELLOW = the number or question being highlighted
  RED    = "no growth" (crossed out)
  PURPLE = mesoderm
  PINK   = endoderm
  BLUE also identifies ectoderm and its derivatives
  YELLOW also identifies inherited factors / signals / graft
  GREY   = outlines, labels, structure
"""
import numpy as np
from bp_style import *  # noqa: F401,F403

ORANGE = "#F29E4C"
BW, BH = 7.4, 4.6   # the zygote block (schematic volume), width x height


def grid(nx, ny, cx=0.0, cy=0.0, w=BW, h=BH, gap=0.08, color=BLUE, op=0.28):
    cw, ch = w / nx, h / ny
    g = VGroup()
    for j in range(ny):
        for i in range(nx):
            x = cx - w / 2 + cw * (i + 0.5)
            y = cy + h / 2 - ch * (j + 0.5)
            r = RoundedRectangle(corner_radius=min(0.12, cw / 4, ch / 4), width=cw - gap, height=ch - gap,
                                 stroke_color=color, stroke_width=2.5, fill_color=color, fill_opacity=op).move_to([x, y, 0])
            g.add(r)
    return g


def dashed_outline(cx=0.0, cy=0.0, w=BW, h=BH, color=GREY):
    r = Rectangle(width=w + 0.2, height=h + 0.2, stroke_color=color, stroke_width=2.5).move_to([cx, cy, 0])
    return DashedVMobject(r, num_dashes=60)


def cross(mob, color=RED):
    return VGroup(Line(mob.get_corner(UL), mob.get_corner(DR), color=color, stroke_width=6),
                  Line(mob.get_corner(DL), mob.get_corner(UR), color=color, stroke_width=6))


def arr(a, b, color=GREY, w=5, tip=0.22):
    return Arrow(a, b, buff=0.08, color=color, stroke_width=w, tip_length=tip,
                 max_tip_length_to_length_ratio=0.45, max_stroke_width_to_length_ratio=12)


def dbar(x0, x1, y, color=YELLOW):
    return VGroup(Line([x0, y, 0], [x1, y, 0], color=color, stroke_width=4),
                  Line([x0, y - 0.15, 0], [x0, y + 0.15, 0], color=color, stroke_width=4),
                  Line([x1, y - 0.15, 0], [x1, y + 0.15, 0], color=color, stroke_width=4))


SEQ = [(1, 1), (2, 1), (2, 2), (4, 2), (4, 4), (8, 4)]


PURPLE = "#B58CD9"
PINK = "#E888AE"


def cell(x=0, y=0, r=0.55, color=BLUE):
    return Circle(radius=r, stroke_color=color, stroke_width=3,
                  fill_color=color, fill_opacity=0.22).move_to([x,y,0])


def layers(x=0, y=0, scale=1):
    # Schematic cross-section, not an anatomical stage or a molecular drawing.
    return VGroup(*[Annulus(inner_radius=r-0.24, outer_radius=r,
                           color=c, fill_opacity=0.55, stroke_width=2)
                    for r,c in [(2.1,BLUE),(1.6,PURPLE),(1.1,PINK)]]).scale(scale).move_to([x,y,0])


def heading(text):
    return T(text, 34, font=TITLE_FONT).move_to([0,3.15,0])


def curve(points, color=BLUE, width=13):
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(
        [np.array([x,y,0]) for x,y in points])


class S00Title(TitleCard):
    LESSON = "Animal development"
    TITLE = "From One Egg to Organized Tissues"

    def construct(self):
        title = T(self.TITLE, 40, font=TITLE_FONT).move_to([0,2.6,0])
        sub = T(self.LESSON.upper(),22,GREY).move_to([0,3.35,0])
        embryo = layers(0,-0.45,0.82)
        rule = Line([-1.2,-2.7,0],[1.2,-2.7,0],color=GOLD,stroke_width=4)
        self.play(FadeIn(sub),Write(title),FadeIn(embryo),Create(rule),run_time=1.2)
        self.finish()


class S01Question(SpokenScene):
    def construct(self):
        q = heading("One egg → organized tissues?")
        egg = cell(-3,0,1.9)
        self.at("How does")
        self.play(FadeIn(q),FadeIn(egg),run_time=0.65)
        self.at("organizes the embryo")
        h=heading("Gastrulation")
        self.play(Transform(q,h),run_time=0.6)
        moving=VGroup(*[cell(-3+1.9*np.cos(a),1.9*np.sin(a),0.18)
                        for a in [0.3,0.9,1.5,2.1]])
        self.at("Cells move from")
        self.play(FadeIn(moving),run_time=0.3)
        self.play(*[m.animate.move_to([-3+dx,dy,0]) for m,dx,dy in
                    zip(moving,[-0.7,0.1,0.6,-0.3],[0.5,0.1,-0.5,-0.7])],run_time=1.7)
        embryo=layers(-3,0)
        self.at("Most animals form")
        self.play(FadeOut(egg),FadeOut(moving),FadeIn(embryo),run_time=0.6)
        labels=[]
        for cue,txt,c,y in [("ectoderm outside","ectoderm · outside",BLUE,1.9),
                            ("mesoderm in the middle","mesoderm · middle",PURPLE,0),
                            ("endoderm inside","endoderm · inside",PINK,-1.9)]:
            lab=T(txt,28,c).move_to([3.0,y,0]); labels.append(lab)
            self.at(cue); self.play(FadeIn(lab),run_time=0.5)
        self.at("In vertebrates")
        self.play(Transform(q,heading("Vertebrate tissue examples")),run_time=0.5)
        for cue,lab,txt,c in [("ectoderm makes",labels[0],"ectoderm → epidermis\nand nervous tissue",BLUE),
                              ("Mesoderm makes",labels[1],"mesoderm → muscle\nand blood",PURPLE),
                              ("Endoderm makes",labels[2],"endoderm → gut\nand airway lining",PINK)]:
            self.at(cue)
            new=T(txt,26,c,line_spacing=0.8).move_to(lab)
            self.play(Transform(lab,new),Indicate(embryo[list(labels).index(lab)],scale_factor=1.04),run_time=0.7)
        self.at("Arranging the cells")
        self.play(Indicate(embryo,scale_factor=1.05),run_time=0.8)
        self.finish()


class S02Count(SpokenScene):
    def construct(self):
        h=heading("Three ways to move inward")
        self.at("The movements differ")
        self.play(FadeIn(h),run_time=0.5)
        xs=[-4.4,0,4.4]
        sheets=[]; labs=[]
        for x,txt in zip(xs,["Invagination","Involution","Ingression"]):
            sheets.append(curve([(x-1.6,0.8),(x,0.8),(x+1.6,0.8)]))
            labs.append(T(txt,26,BLUE).move_to([x,2,0]))
        self.at("In invagination")
        self.play(Create(sheets[0]),FadeIn(labs[0]),run_time=0.45)
        self.at("a sheet bends inward")
        self.play(Transform(sheets[0],curve([(-6,0.8),(-5.3,0.5),(-4.9,-0.8),(-3.9,-0.8),(-3.5,0.5),(-2.8,0.8)])),run_time=1)
        self.at("In involution")
        self.play(Create(sheets[1]),FadeIn(labs[1]),run_time=0.45)
        self.at("it rolls over")
        self.play(Transform(sheets[1],curve([(-1.6,0.8),(0,0.8),(1.4,0.6),(1.5,-0.2),(0.7,-0.7),(-0.6,-0.7)])),run_time=1.4)
        self.at("single cells leave")
        singles=VGroup(*[cell(x,0.8,0.23) for x in [3.1,3.95,4.8,5.65]])
        self.play(FadeIn(labs[2]),FadeIn(singles),run_time=0.4)
        self.play(singles[1].animate.shift(DOWN*1.6+LEFT*0.3),
                  singles[2].animate.shift(DOWN*1.9+RIGHT*0.3),run_time=1.2)
        self.at("Germ layers make tissues")
        self.play(*[FadeOut(m) for m in [*sheets[:2],*labs,singles]],
                  Transform(h,heading("Tissues combine in one intestine")),run_time=0.6)
        outer=Annulus(inner_radius=1.4,outer_radius=2.05,color=PURPLE,fill_opacity=0.45).move_to([-3,0,0])
        inner=Annulus(inner_radius=0.95,outer_radius=1.3,color=PINK,fill_opacity=0.6).move_to([-3,0,0])
        lining=T("endoderm → epithelial lining",26,PINK).move_to([2.5,1.5,0])
        self.at("An intestine has endoderm lining")
        self.play(FadeIn(inner),FadeIn(lining),run_time=0.7)
        muscle=T("mesoderm → muscle\nand connective tissue",26,PURPLE).move_to([2.5,0,0])
        self.at("with mesoderm muscle")
        self.play(FadeIn(outer),FadeIn(muscle),run_time=0.7)
        nerves=VGroup(*[cell(-3+1.7*np.cos(a),1.7*np.sin(a),0.13,BLUE) for a in [0.6,2.8,4.7]])
        nl=T("ectoderm → neural crest\n→ nerve cells",26,BLUE).move_to([2.5,-1.7,0])
        self.at("Neural crest cells")
        self.play(FadeIn(nerves),FadeIn(nl),run_time=0.7)
        self.finish()


class S03Volume(SpokenScene):
    def construct(self):
        h=heading("What sets cell fate?")
        egg=cell(-3,0,1.65)
        self.at("What tells a cell")
        self.play(FadeIn(h),FadeIn(egg),run_time=0.5)
        factors=VGroup(*[Dot([-3+dx,dy,0],radius=0.12,color=YELLOW)
                         for dx,dy in [(-0.6,-0.7),(0,-0.9),(0.6,-0.7)]])
        lab=T("Inherited factors",28,YELLOW).move_to([-3,2.2,0])
        self.at("Cytoplasmic determinants")
        self.play(FadeIn(lab),FadeIn(factors),run_time=0.6)
        self.at("inherited by cells there")
        daughters=VGroup(cell(-3.8,0,0.75),cell(-2,0,0.75))
        self.play(ReplacementTransform(egg,daughters),factors.animate.scale(0.6).move_to([-3.8,0,0]),run_time=1)
        sender=cell(1.3,0,0.65); target=cell(4.5,0,0.8)
        il=T("Neighbouring signal",28,YELLOW).move_to([3,2.2,0])
        signal=arr([2,0,0],[3.6,0,0],YELLOW)
        self.at("Induction is a signal")
        self.play(FadeIn(sender),FadeIn(target),FadeIn(il),GrowArrow(signal),run_time=0.7)
        self.at("changes the fate")
        fate=T("cell fate",24).move_to(target)
        self.play(FadeIn(fate),target.animate.set_fill(BLUE,0.6),run_time=0.6)
        self.at("The amphibian organizer")
        self.play(*[FadeOut(m) for m in [daughters,factors,lab,sender,target,il,signal,fate]],
                  Transform(h,heading("Amphibian organizer graft")),run_time=0.55)
        host=Ellipse(width=5.5,height=4.5,color=BLUE,stroke_width=3,fill_opacity=0.12).move_to([-0.8,-0.25,0])
        axis=Line([-1.8,-1.9,0],[-1.8,1.4,0],color=BLUE,stroke_width=15)
        graft=cell(-5,0.2,0.3,YELLOW)
        gl=T("graft cells",24,YELLOW).move_to([-4.9,1.2,0])
        hl=T("host cells",24,BLUE).move_to([4,1.2,0])
        self.play(FadeIn(host),Create(axis),FadeIn(graft),FadeIn(gl),FadeIn(hl),run_time=0.7)
        self.at("a graft recruited")
        self.play(graft.animate.move_to([0.5,-1.5,0]),run_time=0.6)
        recruited=VGroup(*[cell(x,y,0.18,BLUE) for x,y in [(1.6,-1.3),(1.9,-0.5),(1.7,0.3),(1.2,1)]])
        self.play(FadeIn(recruited),run_time=0.25)
        self.at("second body axis")
        self.play(*[m.animate.move_to([0.5,-0.9+i*0.65,0]) for i,m in enumerate(recruited)],run_time=0.8)
        al=T("second axis",24,BLUE).move_to([4,-0.4,0])
        self.play(FadeIn(al),run_time=0.35)
        self.at("Most embryos studied closely")
        self.play(*[FadeOut(m) for m in [host,axis,graft,gl,hl,recruited,al]],
                  Transform(h,heading("Both inputs help set cell fate")),run_time=0.5)
        left=chip("Inherited factors",YELLOW,28).move_to([-3.2,1,0])
        right=chip("Neighbouring signals",YELLOW,28).move_to([3.2,1,0])
        result=chip("Cell fate",BLUE,32).move_to([0,-1.6,0])
        self.play(FadeIn(left),FadeIn(right),FadeIn(result),
                  GrowArrow(arr(left.get_bottom(),result.get_top()+LEFT*0.4)),
                  GrowArrow(arr(right.get_bottom(),result.get_top()+RIGHT*0.4)),run_time=0.7)
        self.finish()


class S04Size(SpokenScene):
    def construct(self):
        h=heading("Earlier: cleavage")
        egg=cell(0,0,2.1)
        self.at("Earlier cleavage")
        self.play(FadeIn(h),FadeIn(egg),run_time=0.6)
        self.at("the egg divides")
        cuts=VGroup(Line([0,-2.1,0],[0,2.1,0],color=BLUE,stroke_width=3),
                    Line([-2.1,0,0],[2.1,0,0],color=BLUE,stroke_width=3))
        self.play(Create(cuts[0]),run_time=0.65)
        self.play(Create(cuts[1]),run_time=0.65)
        self.at("without growing")
        note=T("same egg outline",26,GREY).move_to([0,-2.8,0])
        self.play(FadeIn(note),run_time=0.5)
        self.at("Each is a blastomere")
        bl=chip("blastomere",BLUE,26).move_to([4,1.1,0])
        pointer=arr(bl.get_left(),[1.1,1.1,0],BLUE)
        self.play(FadeIn(bl),GrowArrow(pointer),run_time=0.6)
        self.at("Yolk slows or blocks")
        self.play(*[FadeOut(m) for m in [egg,cuts,note,bl,pointer]],run_time=0.4)
        # Reused yolk block and divided disc from the original bird comparison.
        yolk=RoundedRectangle(corner_radius=0.2,width=5.4,height=3.2,
                              stroke_color=GOLD,stroke_width=3,fill_color=GOLD,fill_opacity=0.28).move_to([0,-0.65,0])
        yl=T("yolk · undivided",28,GOLD).move_to(yolk)
        self.play(FadeIn(yolk),FadeIn(yl),run_time=0.6)
        self.at("In birds")
        disc=grid(4,1,0,1.3,w=3.5,h=0.65,gap=0.05)
        dl=T("Birds: only the disc divides",28,BLUE).move_to([0,2.2,0])
        self.play(FadeIn(disc),FadeIn(dl),run_time=0.7)
        self.finish()


class S05Membrane(SpokenScene):
    def construct(self):
        h=heading("Starting event: fertilization")
        egg=cell(0,-0.25,2)
        sperm=VGroup(Ellipse(width=0.48,height=0.28,color=BLUE,fill_opacity=0.7),
                     curve([(-0.2,0),(-0.7,0.2),(-1.2,0)],BLUE,3)).move_to([-4,0,0])
        self.at("Fertilization starts")
        self.play(FadeIn(h),FadeIn(egg),FadeIn(sperm),run_time=0.6)
        self.at("Sperm and egg fuse")
        self.play(sperm.animate.move_to([-1.9,-0.25,0]),run_time=0.8)
        self.play(FadeOut(sperm),run_time=0.3)
        z=T("zygote",28,BLUE).move_to([0,-2.9,0])
        self.at("form a zygote")
        self.play(FadeIn(z),run_time=0.4)
        self.at("A calcium wave")
        wave_x=ValueTracker(-1.95)
        wave=always_redraw(lambda: Line([wave_x.get_value(),-0.25-np.sqrt(max(0,4-wave_x.get_value()**2)),0],
                                       [wave_x.get_value(),-0.25+np.sqrt(max(0,4-wave_x.get_value()**2)),0],
                                       color=TEAL,stroke_width=13))
        wl=T("calcium wave",26,TEAL).move_to([-4.5,1.7,0])
        self.add(wave);self.play(FadeIn(wl),wave_x.animate.set_value(1.95),run_time=1.3,rate_func=linear)
        self.remove(wave)
        self.at("restarts the cell cycle")
        cycle=Arc(radius=0.9,start_angle=0.4,angle=TAU-0.7,color=GREEN,stroke_width=6).move_to(egg)
        cycle.add_tip(tip_length=0.2)
        cl=T("cell cycle restarts",26,GREEN).move_to([4,1.5,0])
        self.play(Create(cycle),FadeIn(cl),FadeOut(wl),run_time=0.65)
        self.at("Eggs also block")
        extras=VGroup(*[sperm.copy().set_opacity(1).move_to([3.2,y,0]) for y in [0,-1.1]])
        stops=VGroup(*[Line([2.55,y-0.3,0],[2.55,y+0.3,0],color=RED,stroke_width=7) for y in [0,-1.1]])
        self.play(FadeIn(extras),Create(stops),run_time=0.55)
        self.at("In mice")
        ml=T("Mouse membrane block:\nnon-electrical",26,RED).move_to([4.2,-2.3,0])
        self.play(FadeIn(ml),run_time=0.6)
        self.finish()


class S06Rule(SpokenScene):
    def construct(self):
        h=heading("Frogs, birds and mammals")
        plate=curve([(-3.5,0.4),(-1.8,0.4),(0,0.4),(1.8,0.4),(3.5,0.4)],BLUE,22)
        lab=T("ectoderm → neural plate",28,BLUE).move_to([0,2.1,0])
        self.at("Now follow one tissue")
        self.play(FadeIn(h),Create(plate),FadeIn(lab),run_time=0.6)
        self.at("the neural plate folds")
        folded=curve([(-2.3,1.1),(-1.4,0.6),(-1,-0.9),(0,-1.5),(1,-0.9),(1.4,0.6),(2.3,1.1)],BLUE,22)
        self.play(Transform(plate,folded),run_time=1.1)
        tube=Circle(radius=1,stroke_color=BLUE,stroke_width=22).move_to([0,-0.7,0])
        self.at("a hollow neural tube")
        self.play(ReplacementTransform(plate,tube),
                  Transform(lab,T("hollow neural tube",28,BLUE).move_to(lab)),run_time=0.7)
        future=T("future brain and spinal cord",28,BLUE).move_to([0,-2.4,0])
        self.at("the future brain")
        self.play(FadeIn(future),run_time=0.55)
        self.at("Neural crest forms")
        # Replay the plate to locate crest at its two edges, rather than on the tube.
        crestplate=curve([(-2.3,1.1),(-1.4,0.6),(-1,-0.9),(0,-1.5),(1,-0.9),(1.4,0.6),(2.3,1.1)],BLUE,22)
        crest=VGroup(cell(-2.3,1.1,0.23),cell(2.3,1.1,0.23)).set_stroke(YELLOW,4)
        self.play(FadeOut(tube),FadeOut(future),FadeIn(crestplate),FadeIn(crest),
                  Transform(lab,T("neural crest · plate edges",28,BLUE).move_to(lab)),run_time=0.6)
        self.at("makes peripheral neurons")
        self.play(FadeOut(crestplate),crest.animate.move_to([0,0.5,0]),run_time=0.4)
        neurons=T("Peripheral neurons",27,BLUE).move_to([-3,-1.7,0])
        self.play(FadeIn(neurons),GrowArrow(arr([-1.7,0.1,0],[-3,-1.2,0],BLUE)),run_time=0.55)
        self.at("much of the skeleton")
        skull=T("Much of the facial\nand skull skeleton",27,BLUE).move_to([3,-1.7,0])
        self.play(FadeIn(skull),GrowArrow(arr([1.7,0.1,0],[3,-1.05,0],BLUE)),run_time=0.6)
        self.finish()


class S07End(EndCard):
    LINE = "Cleavage, gastrulation and fate signals turn one egg into tissues."
    def construct(self):
        line=T(self.LINE,40,font=TITLE_FONT).move_to([0,2.8,0])
        fit(line, max_w=12.5)
        embryo=layers(0,-0.2,0.85)
        inherited=chip("Inherited factors",YELLOW,24).move_to([-4.7,0,0])
        signal=chip("Neighbour signals",YELLOW,24).move_to([4.7,0,0])
        sub=T("biochemistrypedia.com",22,TEAL).move_to([0,-3,0])
        self.play(FadeIn(line),FadeIn(embryo),FadeIn(inherited),FadeIn(signal),FadeIn(sub),run_time=1)
        self.finish()
