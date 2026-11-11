"""One carried yeast cell; word cues match audio/words.json.
COLOR MAP: GREY membranes; ORANGE cargo; YELLOW vesicles; BLUE coat;
TEAL Rab/tethers; PURPLE SNARE/SM; PINK GDI; GREEN GTP/success;
RED temperature/block; GOLD ATP. All protein shapes are schematic symbols.
"""
from bp_style import *

ORANGE = "#F29E4C"
PURPLE = "#B58CD9"
PINK = "#E88FB4"


def label(text, x, y, color=TEXT, size=28, width=12.5):
    return fit(T(text, size, color), max_w=width).move_to([x, y, 0])


def packet(x, y, r=0.24):
    ring = Circle(radius=r, color=YELLOW, stroke_width=3,
                  fill_color=YELLOW, fill_opacity=0.08)
    dots = VGroup(*[Dot([dx*r, dy*r, 0], radius=r*0.17, color=ORANGE)
                    for dx, dy in [(-.35, .25), (.35, .2), (0, -.35)]])
    dots.add_updater(lambda m,dt: m.rotate(dt*.35,about_point=m.get_center()))
    return VGroup(ring, dots).move_to([x, y, 0])


class TrafficScene(SpokenScene):
    number = 0

    def moment(self, fraction):
        remaining = self.beat(fraction) - self.elapsed()
        if remaining > .02:
            self.wait(remaining)

    def act(self, *animations, fraction=.07):
        self.play(*animations, run_time=min(.65, self.beat(fraction)))

    def heading(self, text, color=TEXT):
        new = label(text, 0, 3.35, color, 31)
        if hasattr(self, 'head'):
            self.act(ReplacementTransform(self.head, new), fraction=.035)
        else:
            self.add(new)
        self.head = new

    def temperature(self, hot=False, animate=True):
        new = chip('37 °C' if hot else '25 °C', RED if hot else TEXT, size=28)
        new.move_to([-5.25, 2.55, 0])
        if animate:
            self.act(ReplacementTransform(self.thermo, new), fraction=.04)
        else:
            self.remove(self.thermo)
            self.add(new)
        self.thermo = new

    def lamp(self, index, color=GREEN):
        self.play(self.lamps[index].animate.set_color(color).set_fill(color, opacity=1).set_stroke(width=3), run_time=.25)

    def world(self, hot=False, pile=False, lamps=False):
        # Yeast Golgi cisternae are separated, not a mammalian stacked Golgi.
        self.cell = Ellipse(width=10.3, height=5.2, color=GREY, stroke_width=4,
                            fill_color=GREY, fill_opacity=.025).move_to([-.9, -.1, 0])
        self.surface = Arc(radius=2.6, start_angle=-.72, angle=1.44,
                           color=GREY, stroke_width=8).stretch(1.98, 0).move_to([3.65, -.1, 0])
        self.er = VGroup(*[VMobject().set_points_smoothly([
            [-5.1, yy, 0], [-4.65, yy+.18, 0], [-4.15, yy-.15, 0], [-3.65, yy, 0]
        ]).set_stroke(GREY, 7) for yy in [-.85, -.3, .25, .8]])
        self.golgi = VGroup(*[ArcBetweenPoints([x-.4, y, 0], [x+.4, y+.12, 0], angle=.55,
                                              color=GREY, stroke_width=8)
                             for x, y in [(-2, .65), (-1.3, -.7), (-.8, .65)]])
        self.thermo = chip('37 °C' if hot else '25 °C', RED if hot else TEXT, size=28).move_to([-5.25, 2.55, 0])
        self.level = ValueTracker(6 if pile else 1)
        self.fill = always_redraw(lambda: Rectangle(width=.42, height=max(.04, .34*self.level.get_value()),
                                 stroke_width=0, fill_color=ORANGE, fill_opacity=.9)
                                 .move_to([5.55, -1.25+.17*self.level.get_value(), 0]))
        gauge = RoundedRectangle(width=.62, height=2.85, corner_radius=.07,
                                 stroke_color=GREY, stroke_width=2).move_to([5.55, .15, 0])
        self.gauge = VGroup(gauge, self.fill, label('enzyme', 5.45, 2.9, ORANGE, 28),
                            label('inside', 5.45, 2.48, ORANGE, 28),
                            label('schematic', 5.45, -1.7, TEXT, 28))
        self.lamps = VGroup(*[Circle(radius=.18, color=GREY, fill_color=BG, fill_opacity=1)
                             .move_to([x, -3.05, 0]) for x in [-3.8, -.4, 3]])
        names = VGroup(*[label(t, x+.25, -3.05, TEXT, 28).next_to(l, RIGHT, buff=.18)
                         for t, x, l in zip(['budding', 'targeting', 'fusion'], [-3.8, -.4, 3], self.lamps)])
        self.lamp_names = names
        if not lamps:
            names.set_opacity(0)
        self.pile = VGroup(*[packet(x, y) for x, y in [
            (1.05, -.55), (1.25, .15), (1.7, .75), (1.9, -.4),
            (2.4, .25), (2.5, -.85), (1.6, -1.2), (2.2, 1.25)]])
        self.add(self.cell, self.surface, self.er, self.golgi, self.thermo, self.gauge,
                 self.lamps, names,
                 label('ER', -4.1, -1.5, TEXT, 28),
                 label('Golgi', -1.5, -1.65, TEXT, 28),
                 label('surface', 3.6, -2.2, TEXT, 28))
        # A slow membrane contour wave and drifting cisternae keep the actual
        # cell alive while a spoken sentence lands (no decorative particle field).
        self.sway(self.pile)
        for organelle in (self.er,self.golgi):
            self.sway(organelle)
        contour=self.cell.copy()
        self.cell.phase=0
        def breathe(m,dt):
            m.phase+=dt
            pts=contour.get_points().copy()
            pts[:,0]+=.075*np.sin(pts[:,1]*2+m.phase*1.7)
            pts[:,1]+=.065*np.cos(pts[:,0]*1.7+m.phase*1.7)
            m.set_points(pts)
            m.set_fill(opacity=.065+.045*np.sin(m.phase*1.5))
        self.cell.add_updater(breathe)
        if pile:
            self.add(self.pile)

    def sway(self, group):
        for i, obj in enumerate(group):
            anchor = obj.get_center().copy()
            obj.phase = i * .77
            obj.add_updater(lambda m, dt, a=anchor: (
                setattr(m, 'phase', m.phase+dt),
                m.move_to(a+[.10*np.sin(m.phase), .10*np.cos(m.phase), 0])))

    def stream(self, surface=True, fraction=.24):
        """Budding, transit, membrane merger, then cargo release."""
        v = packet(-3.55 if not surface else -.4, 0)
        destination = [4.25, 0, 0] if surface else [-1.65, 0, 0]
        self.act(FadeIn(v, scale=.3), fraction=fraction*.15)
        self.act(v.animate.move_to(destination), fraction=fraction*.6)
        # The vesicle ring opens into the accepting membrane, rather than
        # transporting an intact vesicle through the cell boundary.
        merger = Arc(radius=.28, start_angle=-PI/2, angle=PI, color=YELLOW,
                     stroke_width=4).move_to(destination)
        self.act(ReplacementTransform(v[0], merger), fraction=fraction*.1)
        self.act(FadeOut(merger), v[1].animate.shift(RIGHT*.85), fraction=fraction*.1)
        self.act(FadeOut(v[1]), fraction=fraction*.05)
        self.remove(v, v[0], v[1], merger)

    def release_pile(self):
        # Stagger all eight membrane mergers in a short run, within the spoken cue.
        sequences=[]
        for v in self.pile:
            v.clear_updaters()
            sequences.append(Succession(
                v.animate(run_time=.22).move_to([-.9+5.15*np.sqrt(1-((v.get_y()*.6+.1)/2.6)**2),v.get_y()*.6,0]),
                AnimationGroup(FadeOut(v[0]),v[1].animate.move_to([5.0,v.get_y()*.6,0]),run_time=.22),
                FadeOut(v[1],run_time=.12)))
        self.play(LaggedStart(*sequences,lag_ratio=.13),
                  self.level.animate.set_value(1),run_time=1.2)
        self.remove(self.pile)

    def bracket(self, fusion_only=False):
        x0 = 2.8 if fusion_only else -.6
        return VGroup(Line([x0, -3.45, 0], [4.4, -3.45, 0], color=RED),
                      Line([x0, -3.45, 0], [x0, -3.35, 0], color=RED),
                      Line([4.4, -3.45, 0], [4.4, -3.35, 0], color=RED),
                      label('?', (x0+4.4)/2, -3.64, RED, 28))

    def assay(self, wide=False):
        self.box = DashedVMobject(RoundedRectangle(width=9.3 if wide else 6.2, height=3.6 if wide else 4.2, corner_radius=.15),
                                 num_dashes=45).set_color(GREY).move_to([-.7 if wide else -2.6, -.15 if wide else .05, 0])
        self.add(self.box, label('cell-free', -.7 if wide else 1.7, -2.22 if wide else -.15, TEXT, 28))

    def clock(self):
        self.remove(self.gauge)
        dial = Circle(radius=.6, color=GREY).move_to([5.55, .15, 0])
        hand = Line([5.55, .15, 0], [5.55, .65, 0], color=TEXT)
        self.add(dial, hand, label('schematic', 5.45, -1, TEXT, 28))
        hand.add_updater(lambda m, dt: m.rotate(-dt*.6, about_point=[5.55,.15,0]))
        return hand

    def closeup(self, mode):
        # Keep the carried cell and HUD visible behind a bounded detail panel.
        panel = RoundedRectangle(width=10.0, height=4.65, corner_radius=.15,
                                 fill_color=BG, fill_opacity=1, stroke_color=GREY,
                                 stroke_width=1).move_to([-.7, -.15, 0])
        self.add(panel)
        # Gentle cytosolic shading accompanies continuous membrane/cargo motion.
        panel.phase = 0
        panel.add_updater(lambda m, dt: (setattr(m, 'phase', m.phase+dt), m.set_fill(color=interpolate_color(ManimColor(BG),ManimColor('#24313D'),.13+.11*np.sin(m.phase*1.5))).set_stroke(opacity=.8)))
        if mode == 'coat':
            mem = Line([-5, -.8, 0], [3.5, -.8, 0], color=GREY, stroke_width=9)
            self.add(mem, label('ER lumen', -4, -1.5, GREY), label('cytosol', 2.8, .2, GREY))
            return mem
        v = packet(-2.5, -.15, r=.8)
        target = Line([2.3, -1.7, 0], [2.3, 1.4, 0], color=GREY, stroke_width=10)
        self.sway(VGroup(v[0],target))
        self.vesicle_label=label('vesicle', -3.5, -1.5, YELLOW)
        self.add(v, target, self.vesicle_label, label('surface', 2.3, -2.1, TEXT))
        return v, target

    def snare_strands(self):
        # Qa has a surface anchor; Qb/Qc are linked strands from one protein;
        # R has the vesicle anchor. No transmembrane anchor is drawn for Qb/Qc.
        rods = VGroup(*[Line([-.8, y, 0], [2.3 if i==0 else 1.9, y, 0],
                            color=PURPLE, stroke_width=7)
                         for i, y in enumerate([.65, .2, -.2])],
                      Line([-1.7, -.65, 0], [1.5, -.65, 0], color=PURPLE, stroke_width=7))
        link = Line([1.9, .2, 0], [1.9, -.2, 0], color=PURPLE, stroke_width=7)
        labels = VGroup(*[label(t, -4.7, y, PURPLE, 28)
                          for t, y in zip(['Qa', 'Qb', 'Qc', 'R'], [.65, .2, -.2, -.65])])
        return VGroup(rods, link, labels)

    def construct(self):
        n = self.number
        hot = n in (0, 6, 7, 8, 18, 20)
        piled = n in (0, 4, 6, 7, 8, 18, 19, 20)
        self.world(hot=hot, pile=piled, lamps=n>=6)
        headings = {
            0:'Where do they go?', 2:'The secretory route', 3:'A temperature-sensitive mutant',
            4:'Stored cargo can leave', 5:'Bud. Catch. Fuse.',
            6:'Which job worked? Which failed?', 7:'Which job worked? Which failed?',
            8:'A pile proves budding', 9:'A coat gathers cargo', 10:'COPII: coat on, coat off',
            11:'Budding is not delivery', 12:'Three handoffs. Each can fail alone.',
            13:'Rab: a membrane switch', 14:'Tethers catch the vesicle',
            15:'Four strands, three proteins', 16:'Zip the membranes together',
            17:'SM helps the right zip', 18:'Sec1 helps fusion', 19:'Temperature restores Sec1 function',
            20:'The pile alone cannot tell', 21:'Pile = last place reached',
            22:'Test tubes add timing', 23:'GDI added after docking?',
            24:'GDI-sensitive step: passed', 25:'Bud. Catch. Fuse.'}
        self.heading(headings[n])
        if n == 0:
            self.level.set_value(1)
            self.at('where do the enzymes')
            v=packet(-3.6,0);self.add(v)
            self.play(v.animate.move_to([1.2,0,0]), self.level.animate.set_value(3),run_time=2.2)
            self.at('this yeast mutant')
            self.remove(v);v=packet(-3.6,.5);self.add(v)
            self.play(v.animate.move_to([2.1,.5,0]),self.level.animate.set_value(6),run_time=3.6)
            self.at('but it releases little')
            self.play(Indicate(self.pile,color=YELLOW),run_time=.7)
        elif n == 2:
            self.at('yeasts secrete enzymes')
            route=DashedLine([-4,-1.1,0],[3.3,-1.1,0],color=TEXT)
            self.play(Create(route),run_time=1.8)
            self.at('er then golgi');self.stream(False,.08)
            self.at('then vesicles');self.stream(True,.17)
            self.at('small membrane spheres')
            self.stream(False,.13);self.stream(True,.17)
        elif n == 3:
            self.at('this mutant is called')
            self.add(chip('sec1',YELLOW,size=28).move_to([-.8,1.9,0]))
            self.at('at 25 degrees');self.stream(False,.09);self.stream(True,.12)
            self.at('at 37 degrees');self.temperature(True)
            self.add(self.pile)
            self.play(LaggedStart(*[FadeIn(v,shift=LEFT*.5) for v in self.pile],lag_ratio=.12),run_time=1.1)
            self.at('its enzyme pool inside')
            self.add(label('up to 8×',5.45,1.98,ORANGE,28))
            self.play(self.level.animate.set_value(8),run_time=1.8)
        elif n == 4:
            self.temperature(True,False)
            self.at('the enzymes sit');self.play(Indicate(self.pile,color=YELLOW),run_time=1)
            self.at('back at 25 degrees');self.temperature(False)
            self.at('with protein synthesis blocked')
            self.add(label('protein synthesis blocked',-1.3,1.6,RED,28))
            self.at('the cells secrete them');self.release_pile()
        elif n == 5:
            self.at('every vesicle')
            v=packet(-.6,0);self.add(v)
            self.at('butting pick up cargo')
            self.lamp_names[0].set_opacity(1)
            self.play(v.animate.shift(RIGHT*1.2),run_time=1);self.lamp(0)
            self.at('targeting be caught')
            tether=Line([2.1,0,0],[4.25,0,0],color=TEAL,stroke_width=7)
            self.play(v.animate.move_to([1.85,0,0]),Create(tether),run_time=1)
            self.lamp_names[1].set_opacity(1);self.lamp(1)
            self.at('fusion merge with it')
            self.lamp_names[2].set_opacity(1)
            self.play(v.animate.move_to([4.25,0,0]),FadeOut(tether),run_time=.55)
            self.play(FadeOut(v[0]),v[1].animate.shift(RIGHT*.8),run_time=.5);self.lamp(2)
        elif n in (6,7):
            if n == 6:
                self.at('back to sec 1')
                self.play(self.level.animate.set_value(7),run_time=1.2)
                self.at('which job worked');self.play(Indicate(self.lamps,color=TEXT),run_time=.6)
                self.at('and which could');self.play(Indicate(self.pile,color=YELLOW),run_time=.7)
            else:
                for lamp in self.lamps:
                    lamp.phase=0
                    lamp.add_updater(lambda m,dt:(setattr(m,'phase',m.phase+dt),m.set_stroke(opacity=.6+.3*np.sin(m.phase))))
        elif n == 8:
            self.at('butting worked');self.lamp(0)
            self.add(label('✓',-3.8,-2.62,GREEN,28))
            self.at('targeting or fusion');self.play(Create(self.bracket()),run_time=.7)
            self.at('a pile of vesicles alone');self.play(Indicate(self.pile,color=YELLOW),run_time=.7)
        elif n in (9,10,11):
            mem=self.closeup('coat')
            cargo=VGroup(*[Dot([x,-1.15,0],radius=.1,color=ORANGE) for x in [-1.4,-.8,-.2,.4]])
            coat=VGroup(*[RoundedRectangle(width=.7,height=.27,corner_radius=.08,color=BLUE,fill_color=BLUE,fill_opacity=.5).move_to([x,.35,0]) for x in [-1.4,-.7,0]])
            self.add(cargo)
            bud=VGroup(Line([-5,-.8,0],[-1.6,-.8,0],color=GREY,stroke_width=9),
                Arc(radius=.8,start_angle=0,angle=PI,color=GREY,stroke_width=9).move_to([-.8,-.2,0]),
                Line([0,-.8,0],[3.5,-.8,0],color=GREY,stroke_width=9))
            if n == 9:
                self.at('a coat of proteins');self.play(FadeIn(coat,shift=DOWN*.4),run_time=1.2)
                self.at('it bends a bud')
                hands=VGroup(*[Line([x,.25,0],[x,-.35,0],color=BLUE,stroke_width=4) for x in [-1.4,-.7,0]])
                carriers=VGroup(*[Line([x,-.55,0],[x,-.95,0],color=GREY,stroke_width=6) for x in [-1.4,-.7,0]])
                self.play(Transform(mem,bud),FadeIn(hands),FadeIn(carriers),cargo.animate.move_to([-.8,-.35,0]),run_time=.9)
                self.add(label('coat',-.8,1.35,BLUE,28))
                self.at('grabs the cargo');self.play(cargo.animate.shift(UP*.2),run_time=.5)
            else:
                mem.become(bud)
                self.add(coat,label('COPII',-2.8,1.35,BLUE,28))
                if n == 10:
                    self.at('a switch called')
                    badge=chip('Sar1 · GTP',GREEN,size=28).move_to([.8,1.35,0]);self.add(badge)
                    self.at('pulls it on');self.play(coat.animate.shift(DOWN*.2),run_time=.6)
                else:
                    self.assay(wide=True);self.at('gtp analog')
                    badge=chip('GTP analogue · locked',GREEN,size=28).move_to([1.6,1.15,0]);self.add(badge)
                    self.at('still butted')
                v=packet(-.8,-.1,.55)
                ring=DashedVMobject(Circle(radius=.72,color=BLUE,stroke_width=6),num_dashes=15).move_to(v)
                self.play(FadeIn(v),FadeIn(ring),FadeOut(cargo),FadeOut(coat),Transform(mem,Line([-5,-.8,0],[3.5,-.8,0],color=GREY,stroke_width=9)),run_time=.5)
                self.lamp(0)
                if n == 10:
                    self.at('when sar 1 hydrolyzes')
                    self.play(Transform(badge,chip('Sar1 · GDP',TEXT,size=28).move_to(badge)),run_time=.6)
                    self.at('the coat begins')
                    self.play(ring.animate.scale(1.4).shift(UP*.2).set_opacity(0),run_time=1)
                else:
                    self.at('but they kept their coat')
                    self.play(VGroup(v,ring).animate.shift(RIGHT*2),run_time=1)
                    self.at('failed to target');self.lamp(1,RED)
                    self.at('making a vesicle');self.play(Indicate(v,color=YELLOW),run_time=.7)
        elif n == 12:
            self.at('here is the one idea')
            v=packet(-.6,0);self.add(v)
            self.at('a coat buds it')
            badge=chip('coat',BLUE,size=28).move_to([-.8,1.65,0]);self.add(badge)
            self.play(v.animate.shift(RIGHT),run_time=.7);self.lamp(0)
            self.at('a rabb and a tether')
            self.play(Transform(badge,chip('Rab + tether',TEAL,size=28).move_to(badge)),v.animate.move_to([2.7,0,0]),run_time=.6)
            tether=Line([2.9,0,0],[4.25,0,0],color=TEAL,stroke_width=7);self.add(tether);self.lamp(1)
            self.at('snares guided by')
            self.play(Transform(badge,chip('SNAREs + SM protein',PURPLE,size=28).move_to(badge)),run_time=.6)
            self.at('fuse it');self.play(v.animate.move_to([4.25,0,0]),FadeOut(tether),run_time=.35)
            self.play(FadeOut(v[0]),v[1].animate.shift(RIGHT*.8),run_time=.4);self.lamp(2)
        elif n in (13,14):
            v,target=self.closeup('rab')
            rab=chip('Rab',TEAL,size=28).move_to([-.9,.6,0])
            tail=Line([-1.7,.4,0],[-1.3,.6,0],color=TEAL,stroke_width=5)
            badge=chip('GDP' if n==13 else 'GTP',TEXT if n==13 else GREEN,size=28).move_to([-.7,1.45,0])
            self.add(rab,tail,badge)
            if n==13:
                VGroup(rab,tail,badge).shift(RIGHT*.5)
                self.at('a rab is a small switch');self.play(Indicate(tail,color=TEAL),run_time=.7)
                self.at('holding gdp')
                cup=Arc(radius=.7,start_angle=0,angle=-PI,color=PINK,stroke_width=6).move_to([-.3,.55,0])
                gdil=label('GDI',-3,1.5,PINK,28)
                self.add(cup,gdil)
                self.at('at the right membrane')
                self.play(FadeOut(cup,shift=UP*.7),FadeOut(gdil),VGroup(rab,tail,badge).animate.shift(LEFT*.5),run_time=.7)
                self.at('an exchange factor')
                exchange=chip('exchange factor',TEXT,size=28).move_to([0,-1.3,0]);self.add(exchange)
                self.at('loads gtp')
                self.play(Transform(badge,chip('GTP',GREEN,size=28).move_to(badge)),run_time=.6)
            else:
                self.at('rab with gtp');self.play(Indicate(rab,color=TEAL),run_time=.8)
                tether=VGroup(*[RoundedRectangle(width=.48,height=.25,corner_radius=.06,color=TEAL,fill_color=TEAL,fill_opacity=.5).move_to([x,0,0]) for x in [-.9,-.45,0,.45,.9,1.35,1.8]])
                self.at('it recruits tethers');self.play(FadeIn(tether,shift=DOWN*.4),run_time=.8)
                self.at('which catch the vesicle');self.lamp(1)
                self.at('one sign among several')
                patch=Line([2.3,.6,0],[2.3,.95,0],color=TEAL,stroke_width=12)
                stub=Line([2,.35,0],[2.3,.35,0],color=PURPLE,stroke_width=7)
                self.play(FadeIn(patch),FadeIn(stub),run_time=.5)
        elif n in (15,16,17):
            v,target=self.closeup('snare');strands=self.snare_strands()
            if n==15:
                self.at('two membranes resist')
                shimmer=DashedLine([.2,-1.1,0],[.2,1.15,0],color=TEXT);self.add(shimmer)
                shimmer.phase=0
                shimmer.add_updater(lambda m,dt:(setattr(m,'phase',m.phase+dt),m.set_stroke(opacity=.5+.4*np.sin(3*m.phase))))
                self.at('snare proteins supply');self.add(label('SNAREs',-.7,1.65,PURPLE,28))
                self.at('four strands');self.play(FadeIn(strands[0]),FadeIn(strands[1]),run_time=.5)
                self.at('called qa');self.play(FadeIn(strands[2]),run_time=.5)
            else:
                self.add(strands)
                if n==17:
                    self.at('in the main fusion steps studied')
                    self.at('an sm protein')
                    self.add(chip('SM protein',PURPLE,size=28,fill_opacity=0).move_to([-.7,1.65,0]))
                    self.at('it binds them')
                else:self.at('they zip into one rope')
                # Four schematic protein strands zip into a bundle; no molecular structure.
                rope=VGroup(*[Line([-1.5,dy,0],[2.3,dy,0],color=PURPLE,stroke_width=6) for dy in [-.15,-.05,.05,.15]])
                self.play(FadeOut(strands[2]),ReplacementTransform(VGroup(strands[0],strands[1]),rope),run_time=1.2)
                if n==16:self.at('the zipping pulls')
                else:self.at('helps the right four')
                v[0].clear_updaters();target.clear_updaters()
                self.play(v.animate.shift(RIGHT*2.1),run_time=1)
                if n==16:self.at('until they fuse')
                self.play(v.animate.move_to([2.3,0,0]),run_time=.35)
                self.play(FadeOut(v[0]),FadeOut(rope),FadeOut(self.vesicle_label),v[1].animate.shift(RIGHT*1),run_time=.5);self.lamp(2)
                if n==16:
                    self.at('the zip itself')
                    atp=chip('ATP',GOLD,size=28).move_to([-.7,1.65,0]);self.add(atp)
                    self.at('no atp');self.play(Create(Cross(atp,stroke_color=GOLD)),run_time=.4)
        elif n==18:
            self.at('sec1 is the sm protein')
            self.add(chip('Sec1 · SM protein',PURPLE,size=28,fill_opacity=0).move_to([-1.2,1.65,0]))
            self.lamp(0);b=self.bracket();self.add(b)
            self.at('that step is fusion');self.play(Transform(b,self.bracket(True)),run_time=.9)
        elif n==19:
            self.temperature(True,False)
            sm=chip('Sec1',RED,size=28).move_to([-1.2,1.65,0]);self.add(sm)
            self.at('vesicles still bud');self.lamp(0)
            self.play(self.level.animate.set_value(8),run_time=.7)
            self.at('back at 25');self.temperature(False)
            self.at('sec 1 works again');self.play(sm.animate.set_color(PURPLE),run_time=.4)
            self.at('the stored vesicles fuse');self.release_pile();self.lamp(2)
        elif n==20:
            self.at('but the pile alone');self.add(label('docking unknown',-.8,1.95,TEXT,28))
            badge=chip('Rab',TEAL,size=28).move_to([.5,1.25,0]);fault=label('×',1.55,1.8,RED,40)
            self.at('a failed rab');self.add(badge,fault)
            self.at('tether');self.play(Transform(badge,chip('tether',TEAL,size=28).move_to(badge)),run_time=.2)
            self.at('or snare');self.play(Transform(badge,chip('SNARE',PURPLE,size=28).move_to(badge)),run_time=.3)
            self.at("sec1's known job");self.play(Transform(badge,chip('Sec1',PURPLE,size=28).move_to(badge)),run_time=.5)
        elif n==21:
            self.at('on a linear route')
            block=Line([-3.4,-1.1,0],[-3.4,1.1,0],color=RED,stroke_width=8);self.add(block)
            self.at('cargo piles up')
            cargo=VGroup(*[Dot([-4.6+(i%4)*.22,-.55+(i//4)*.3,0],radius=.09,color=ORANGE) for i in range(12)])
            self.play(FadeIn(cargo),run_time=.8);self.sway(cargo)
            self.at('double mutants');self.play(Create(Line([3.4,-1.1,0],[3.4,1.1,0],color=RED,stroke_width=8)),run_time=.7)
        elif n in (22,23,24):
            self.assay();self.clock()
            v=packet(-2.8,-.15,.3);self.add(v)
            rab=chip('Rab · GDP' if n==22 else 'Rab · GTP',TEAL,size=28).move_to([-2.0,1.55,0]);self.add(rab)
            tether=Line([-2.3,-.15,0],[-1.65,-.15,0],color=TEAL,stroke_width=6)
            if n==22:
                self.at('gdi which pulls')
                gdi=chip('GDI',PINK,size=28).move_to([-3.8,1.55,0]);self.add(gdi)
                self.play(VGroup(gdi,rab).animate.shift(RIGHT*.2),run_time=1)
                self.at('blocks fusion');self.lamp(2,RED)
                self.at('what if it is added')
                self.remove(gdi,rab);self.lamps[2].set_color(GREY).set_fill(BG,opacity=1)
                self.heading('GDI added after docking?')
            elif n==23:
                self.play(v.animate.move_to([-2,-.15,0]),Create(tether),run_time=2)
                self.lamp(1)
            else:
                v.move_to([-2,-.15,0]);self.add(tether);self.lamps[1].set_color(GREEN).set_fill(GREEN,opacity=1)
                self.at('its effect fades')
                gdi=chip('GDI',PINK,size=28).move_to([-.1,1.55,0]);self.add(gdi)
                self.play(gdi.animate.shift(DOWN*.2),run_time=.6)
                self.play(gdi.animate.shift(UP*.2),run_time=.6)
                self.at('once vesicles had docked')
                self.play(v.animate.move_to([-1.65,-.15,0]),run_time=.7)
                self.at('fusion was no longer sensitive')
                self.play(FadeOut(v[0]),v[1].animate.shift(RIGHT*.6),FadeOut(tether),run_time=.8);self.lamp(2)
                self.at('a fast specific inhibitor');self.play(Indicate(gdi,color=PINK),run_time=.7)
        elif n==25:
            self.at('so each vesicle');self.stream(False,.1);self.stream(True,.14)
            self.at('bud catch fuse')
            for i in range(3):self.lamp(i)
            self.at('anyone can fail')
            self.lamps[1].set_color(GREY).set_fill(BG,opacity=1)
            self.lamps[2].set_color(GREY).set_fill(BG,opacity=1)
            self.lamp(0,RED);d=Dot([-4.3,0,0],radius=.16,color=ORANGE);self.add(d)
            self.play(d.animate.shift(UP*.3),run_time=.5)
            self.lamp(0);self.remove(d);self.stream(False,.07)
            self.at('where cargo stalls')
            b=self.bracket();self.add(b);self.lamp(1,RED);self.lamp(2,RED)
            self.add(self.pile);self.play(self.level.animate.set_value(7),run_time=.5)
            self.at('help place the break')
            self.lamp(1);self.lamp(2);self.remove(b);self.release_pile()
        if n in (7,23):
            remaining=self.narration_s-self.elapsed()
            if remaining>0:self.wait(remaining)
        else:self.finish()


class S00Hook(TrafficScene):
    number = 0

class S01Title(TitleCard, TrafficScene):
    TITLE = 'Three Handoffs for a Vesicle'
    LESSON = 'Vesicle Budding, Targeting and Fusion'

    def construct(self):
        self.world(hot=True,pile=True)
        overlay=Rectangle(width=14.1,height=7.9,fill_color=BG,fill_opacity=.65,stroke_width=0)
        title=fit(T(self.TITLE,size=46,font=TITLE_FONT),max_w=12.5).move_to([0,.35,0])
        self.add(overlay,title,label(self.LESSON,0,-.6,TEXT,28))
        self.wait(2)

class S02Route(TrafficScene):
    number = 2

class S03Sec1(TrafficScene):
    number = 3

class S04Pile(TrafficScene):
    number = 4

class S05Jobs(TrafficScene):
    number = 5

class S06Predict(TrafficScene):
    number = 6

class S07Think(TrafficScene):
    number = 7

class S08Reveal(TrafficScene):
    number = 8

class S09Coat(TrafficScene):
    number = 9

class S10Sar1(TrafficScene):
    number = 10

class S11Analogue(TrafficScene):
    number = 11

class S12Idea(TrafficScene):
    number = 12

class S13Rab(TrafficScene):
    number = 13

class S14Tether(TrafficScene):
    number = 14

class S15Snare(TrafficScene):
    number = 15

class S16Zip(TrafficScene):
    number = 16

class S17Sm(TrafficScene):
    number = 17

class S18Answer(TrafficScene):
    number = 18

class S19Why(TrafficScene):
    number = 19

class S20Caution(TrafficScene):
    number = 20

class S21Rule(TrafficScene):
    number = 21

class S22GdiQ(TrafficScene):
    number = 22

class S23Think(TrafficScene):
    number = 23

class S24GdiAnswer(TrafficScene):
    number = 24

class S25Return(TrafficScene):
    number = 25

class S26End(EndCard):
    LINE = 'Bud, catch, fuse: three handoffs, and each can fail alone.'
