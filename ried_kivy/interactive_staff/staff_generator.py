from kivy.lang import Builder
from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.clock import Clock

from ried.bar.bar_generator import Bar
from ried.beat.beat_generator import Beat
from ried.note.note_generator import Note, Silence
from ried.chord.chord_generator import Chord

from functools import partial
import os

string = '''
#:import os os
<InteractiveStaff>
    size_hint:None, None
    #pos_hint: {'center_x': 0.5, 'center_y':0.5}
    size: 800, 200
    clave: 'sol'

    LineStaff:
        disabled: True
        size: self.parent.width - 20, 9
        id: central
        pos: 10, self.parent.height/2


<SpaceStaff>
    size_hint:None, None
    shadowed: False  
    canvas.before:
        Color:
            rgba: [1, 0, 0, 0.3] if self.shadowed == 1 else [1, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos

<Barline>
    size_hint:None, None
    size: 8, 64
    shadowed: False  
    canvas.before:
        Color:
            rgba: [1, 0, 0, 0.3] if self.shadowed == 1 else [1, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
    canvas:
        Color:
            rgb: 0,0,0
            a: 1 if self.disabled == False else 0 
        Line:
            points: self.pos[0] + 5, self.pos[1], self.pos[0] + 5, self.pos[1] + self.height
            

<LineStaff>
    canvas:
        Color:
            rgb: 0,0,0
            a: 1 if self.disabled == False else 0 
        Line:
            points: [self.pos[0], self.pos[1] + (self.height/2), self.pos[0] + self.width, self.pos[1] + (self.height/2)]

<AditionalLine>
    canvas:
        Color:
            rgb: 0,0,0
            a: 1 if self.disabled == False else 0 
        Line:
            points: [self.pos[0], self.pos[1] + self.height/2, self.pos[0] + self.width, self.pos[1] + (self.height/2)]

<Clave>
    size_hint: None, None
    height: 130
    shadowed: False  
    canvas.before:
        Color:
            rgba: [1, 0, 0, 0.3] if self.shadowed == 1 else [1, 0, 0, 0]
        Rectangle:
            size: self.size
            pos: self.pos
    color: [0,0,0,1] 
    disabled_color: [0,0,0,0]
    font_size: 130
    #font_name: os.sep.join([os.getcwd(), 'ried_kivy', 'interactive_staff', 'RIED_V5.otf'])
    font_name: 'RIED_V5.otf'

<Neuma>
    size: 22, 16
    text: 's'
    font_size: 135
    text_size: self.size[0], 158
    valign: 'top'

<BarNum>
    height: 48
    text_size: self.size[0], 158
    valign: 'bottom'
    halign: 'center'

<Alter>
    text_size: self.size[0], 158
    valign: 'middle'
    halign: 'center'

<PlicaDown>
    size_hint:None, None
    width: 8
    canvas:
        Color:
            rgb: 0,0,0
            a: 1 if self.disabled == False else 0 
        Line:
            points: self.pos[0]+2, self.pos[1], self.pos[0]+2, self.pos[1] - self.height

<PlicaUp>
    size_hint:None, None
    width: 8
    canvas:
        Color:
            rgb: 0,0,0
            a: 1 if self.disabled == False else 0 
        Line:
            points: self.pos[0]+20, self.pos[1]+7, self.pos[0]+20, self.pos[1] + self.height + 7

<JoinerUp>
    size_hint:None, None
    canvas:
        Color:
            rgb: 0,0,0
            a: 1 if self.disabled == False else 0 
        Rectangle:
            pos: self.pos[0]+20, self.pos[1] + 3
            size: self.width + 1, self.height

<JoinerDown>
    size_hint:None, None
    canvas:
        Color:
            rgb: 0,0,0
            a: 1 if self.disabled == False else 0 
        Rectangle:
            pos: self.pos[0]+2, self.pos[1] - 3
            size: self.width + 1, self.height

'''

Builder.load_string(string)


class SpaceStaff(Label):
    pass

class Barline(Label):
    pass

class LineStaff(SpaceStaff):
    pass

class AditionalLine(SpaceStaff):
    pass

class Clave(Label):
    pass

class Neuma(Clave):
    pass

class BarNum(Clave):
    pass

class Alter(Clave):
    pass

class PlicaUp(Label):
    pass

class PlicaDown(Label):
    pass

class JoinerUp(Label):
    pass

class JoinerDown(Label):
    pass

class InteractiveStaff(RelativeLayout):
    '''
    la
    '''
    
    dictClefs = {8: {'sol': {'text':'z', 'width':40}, 'fa':{'text':'x', 'width':45}, 'do':{'text':'c', 'width':43}, 'perc':{'text':'v', 'width':20}}}
    dictClefsPos = {8:(7*8)-(8//4), 9:(9*7)-(9//4), 'do':'c', 'perc':'v'}
    dictMeasure = {8:{'width': 28}}
    dictAlter = {8: {'displace':20,'flat':{'width': {1:13, 2:24}, 'height':36, \
            'pos': {'sol':{1:[],\
                            2:[0,3,-1,2,-2,1,-3], \
                            3:[], 4:[], 5:[]}, \
                    'fa':{1:[], 2:[], 3:[], 4:[-2,1,-3,0,-4,-1,-5], 5:[]}, \
                    'do': {1:[], 2:[], 3:[], 4:[], 5:[]}}\
                    }, \
            'sharp':{'width':{1:18, 2:17}, 'height':37, \
            'pos': {'sol':{1:[],\
                            2:[4,1,5,2,-1,3,0], \
                            3:[], 4:[], 5:[]}, \
                    'fa':{1:[], 2:[], 3:[], 4:[2,-1,3,0,-3,1,-2], 5:[]}, \
                    'do': {1:[], 2:[], 3:[], 4:[], 5:[]}}}}\
                    }
    element_padding = 6
    spaceH_Barline = {8:5}
    dict_silences = {4:{'str':'q', 'height': 140}, 2:{'str':'w', 'height': 140}, 1:{'str':'e', 'height': 140}, 0.5:{'str':'r', 'height': 151}, 0.25:{'str':'t', 'height': 165}, 0.125:{'str':'y', 'height': 140}, 0.0625:{'str':'u', 'height': 140}}
    dictFlags = {'up': {'pos_x':{8: 18}, 'pos_y':{8:-30}, 'str':{0.5:'d', 1/4:'f', 1/8:'g', 1/16:'h', 1/32:'j'}}, 'down': {'pos_x' : {8: 1}, 'pos_y':{8:40}, 'str': {0.5:'D', 1/4:'F', 1/8:'G', 1/16:'H', 1/32:'J'}}}

    def init_staff(self, lines=5, addUp=3, addDown=5, clef='sol', clef_pos=2, neuma=True, space=8, measure=None, alter=0, align='left', content=None, margin_system=10, beamless=False):
        '''
        update the layout of the interactive Staff
        Since lines position are base on the height and width of the widget, it is necessary to make the update after the window is created
        This update allows to the interactive Staff loads only the needed amount of lines, adtional lines, clefs
        Aditionally, the space among lines is set here.

        '''
        self._check_values(lines, addUp, addDown, clef, clef_pos, neuma, space, measure, alter, align)
        self.space = space
        self.clef = clef
        self.clef_pos = clef_pos
        self.margin_system = margin_system
        self.cursor = margin_system * 1
        self.measure = measure
        self.alter = alter
        self.content = content
        self.beamless = beamless
        self.align = self._set_align(align)
        self._create_elements(lines, addUp, addDown, neuma, 0)
        #Clock.schedule_once(partial(self._create_elements, lines, addUp, addDown, neuma), 1)
    
    def _set_align(self, align):
        if align == 'center':
            if len(self.content) == 1 and len(self.content[0].content) == 1 and len(self.content[0].content[0].content) == 1:
                return 'center'
        return 'left'

    def _create_elements(self, lines, addUp, addDown, neuma, clock):
        self.get_lines = {}
        self._create_lines(lines)
        #self._create_additional_lines(addUp, addDown)
        self._create_clef()
        self._set_key()
        self._create_bar_sig()
        self._display_content()

    def _check_values(self, lines, addUp, addDown, clef, clef_pos, neuma, space, measure, alter, align):
        if not isinstance(lines, int) or lines < 0:
            raise ValueError('lines must be "int" >= 0')
        if not isinstance(addUp, int) or addUp < 0:
            raise ValueError('addUp must be "int" >= 0')
        if not isinstance(addDown, int) or addDown < 0:
            raise ValueError('addDown must be "int" >= 0')
        if clef and clef.lower() not in ['sol', 'do', 'fa', 'perc']:
            raise ValueError('clef must be any of "sol", "do", "fa", "perc"')
        if clef_pos and not isinstance(clef_pos, int):
            raise ValueError('clef_pos must be "int"')
        if not isinstance(neuma, bool):
            raise ValueError('neuma must be "bool"')
        if not isinstance(space, int):
            raise ValueError('space must be "int"')
        if measure and not isinstance(measure, str):
            raise ValueError('measure must be "int"')
        if alter and not isinstance(alter, int):
            raise ValueError('alter must be "int"')
        if align and align.lower() not in ('left', 'right', 'center'):
            raise ValueError('align must be any of  "left", "right", "center"')

    def _create_lines(self, lines):
        self.get_lines['lines'] = []
        if not lines:
            self.get_lines['lines'].append(self.ids.central)
            return
        lowerlines = ((lines - 1) // 2) * -1
        upperlines = lines - 1 + lowerlines
        for x in range(lowerlines, upperlines + 1):
            if x == 0:
                self.get_lines['lines'].append(self.ids.central)
                continue
            l = LineStaff(size=self.ids.central.size)
            self.add_widget(l)
            self.ids.central.disabled = False
            l.pos = self.ids.central.pos[0], self.ids.central.pos[1]  + ((self.space * 2) * x)
            self.get_lines['lines'].append(l)

    def _create_additional_lines(self, addUp, addDown):
        self.get_lines['additional'] = {}
        if addUp:
            self.get_lines['additional']['up'] = []
            for x in range(addUp):
                l = AditionalLine(size=[self.space*4, self.ids.central.height])
                self.add_widget(l)
                l.pos = (self.width/2) - (l.width/2), self.get_lines['lines'][-1].pos[1] + ((x+1) * self.space * 2) 
                self.get_lines['additional']['up'].append(l)
        if addDown:
            self.get_lines['additional']['down'] = []
            for x in range(addDown):
                l = AditionalLine(size=[self.space*4, self.ids.central.height])
                self.add_widget(l)
                l.pos = (self.width/2) - (l.width/2), self.get_lines['lines'][0].pos[1] - ((x+1) * self.space * 2) 
                self.get_lines['additional']['down'].append(l)

    def _create_clef(self):
        if self.clef:
            self.clef_symbol = Clave(text=self.dictClefs[self.space][self.clef]['text'])
            self.clef_symbol.width = self.dictClefs[self.space][self.clef]['width'] + self.element_padding
            self.add_widget(self.clef_symbol)
            self.clef_symbol.pos = self.cursor, self.ids.central.pos[1] - self.dictClefsPos[self.space]
            self.cursor += self.clef_symbol.width 

    def _set_key(self):
        self.alterNotes = self.alter > 0 and {x:0 for x in 'FCGDAEB'} or {x:0 for x in 'BEADGCF'}
        if self.alter:
            if self.alter > 14 or self.alter < -14:
                raise ValueError(f'alter must be a int between -14 and 14')
            for x in range(abs(self.alter)):
                if x >= len(self.alterNotes):
                    x %= 7
                self.alterNotes[list(self.alterNotes.keys())[x]] += 1
            for i, l in enumerate(self.alterNotes.values()):
                if not l:
                    continue
                key = self.alter < 0 and 'flat' or 'sharp'
                if key == 'flat':
                    text = l == 1 and 'b' or 'B'
                else:
                    text = l == 1 and 'n' or 'N'
                size = self.dictAlter[self.space][key]['width'][l], self.dictAlter[self.space][key]['height']
                pos = self.cursor, self.ids.central.pos[1] + self.space * self.dictAlter[self.space][key]['pos'][self.clef][self.clef_pos][i]
                self._print_alter(text, size, pos)
                self.cursor += size[0]

    def _print_alter(self, text, size, pos):
        symbol = Alter()
        symbol.text = text
        symbol.size = size
        symbol.pos = pos
        self.add_widget(symbol)

    def _create_bar_sig(self):
        if self.measure:
            sep = [x for x in self.measure if not x.isdigit()]
            if len(sep) > 1:
                raise ValueError('measure separator not valid {measure}')
            nume, deno = self.measure.split(sep[0])
            self.nume = BarNum(text=nume, pos=(self.cursor, self.ids.central.pos[1]))
            self.deno = BarNum(text=deno, pos=(self.cursor, self.ids.central.pos[1]-(self.space*4)))
            length = max([len(x) for x in (nume, deno)])
            self.nume.width = (self.dictMeasure[self.space]['width'] * length) + self.element_padding
            self.deno.width = (self.dictMeasure[self.space]['width'] * length) + self.element_padding
            self.add_widget(self.nume)
            self.add_widget(self.deno)
            self.cursor += self.nume.width
        self.cursor += 40
        if self.width == 200 and self.content and isinstance(self.content[0].content[0].content[0], Chord):
            alter = sum([abs(x.alter) for x in self.content[0].content[0].content[0].content])
            if alter > 1: 
                alter -= 1
                self.cursor += 15 * alter

    def _display_content(self):
        if self.content:
            self._check_content()
            self._set_content_hSpace()
            self._print_neumas()
            if not self.beamless:
                self._print_joiners_and_flags()

    def _check_content(self):
        error = None
        if isinstance(self.content, (tuple, list)):
            if isinstance(self.content[0], (Bar, Beat)):
                if not any([isinstance(x, Bar) for x in self.content] + [isinstance(x, Beat) for x in self.content]):
                    error = True
            elif isinstance(self.content[0], (Chord, Note)):
                if not all([isinstance(x, (Chord, Note)) for x in self.content]):
                    error = True
        elif not isinstance(self.content, (Bar, Beat, Note, Chord)):
            error = True
        else:
            self.content = [self.content]
        if error:
            raise ValueError(f'{self.content} is not valid to display')
        self.total_bars = 0
        for bar in self.content:
            if isinstance(bar, Beat):
                raise ValueError(f'En staff_generator falta covertir Beat to Bar para que el código corra bien')
            if isinstance(bar, Note):
                raise ValueError(f'En staff_generator falta covertir Note to Beat para que el código corra bien')
            if isinstance(bar, Silence):
                raise ValueError(f'En staff_generator falta covertir Silence to Beat para que el código corra bien')
            self.total_bars += 1

    def _set_content_hSpace(self):
        figures = {}
        for bar in self.content:
            for beat in bar.content:
                for fig in beat.content:
                    if fig.duration not in figures:
                        figures[fig.duration] = 1
                    else:
                        figures[fig.duration] += 1
        figures = self._get_width(figures)
        width_available = self.width - self.margin_system - self.cursor - (self.spaceH_Barline[self.space] * (self.total_bars - 1))
        for bar in self.content:
            for beat in bar.content:
                for fig in beat.content:
                    fig.graph = {'width': width_available * figures[fig.duration]['width']}
        del figures

    def _get_width(self, figures):
        total = sum([value*self._proportion(1/key) for key, value in figures.items()])
        for key, value in figures.items():
            figures[key] = {'amount': value, 'width':self._proportion(1/key) / total}
        return figures

    def _proportion(self, n):
        low, hi, pw = None, None, 1
        while True:
            if 2**pw <= n:
                low = pw
            if 2**pw >= n:
                hi = pw
                if not low:
                    low = 1
                    while 2** low > n:
                        low -= 0.1
                break
            pw += 1
        if low == hi:
            answer = (18 - 3*pw)/32
        else:
            porce = (n - 2**low)/(2**hi - 2**low)
            span = (18-3*low) - (18-3*hi)
            value = span * porce
            answer = ((18-3*low) - value)/32
        return (100-(100*answer))/n

    def _print_neumas(self):
        for bar in self.content:
            for beat in bar.content:
                beat.neumas = []
                if hasattr(beat, 'border_notes'):
                    direction = [beat.beam_direction, beat.border_notes]
                    for fig in beat.content:
                        if isinstance(fig, Chord):
                            self._secondsChordPos(fig, direction[0])
                            self._accidentalChordPos(fig)
                            for i, sound in enumerate(fig.content, 1):
                                if (direction[0] == 'up' and i == 1) or (direction[0] == 'down' and i == len(fig.content)):
                                    self._create_neuma(beat, fig, sound, direction)
                                else:
                                    self._create_neuma(beat, fig, sound)
                        elif isinstance(fig, Note):
                            fig.displace = 0
                            fig.alterpos = 0
                            self._create_neuma(beat, fig, fig, direction)
                        else:
                            self._create_silence(beat, fig)
                        self.cursor += fig.graph['width']
                else:
                    self._create_silence(beat, beat.content[0])
                    self.cursor += beat.content[0].graph['width']

    def _secondsChordPos(self, chord, direction):
        displace = direction == 'down' and -1 or 1
        content = direction == 'down' and chord.content[::-1] or chord.content
        content[0].displace = 0
        for i, note in enumerate(content[1:], 1):
            interval = note ^ content[i-1]
            if '2' in interval.intervalNotation:
                if not content[i-1].displace:
                    note.displace = displace
                    if displace < 0 and not hasattr(chord, 'displace'):
                        chord.displace = 18
                else:
                    note.displace = 0
            else:
                note.displace = 0
        if not hasattr(chord, 'displace'):
            chord.displace = 0


    def _accidentalChordPos(self, chord):
        response = [x for x in chord.content if x.alter]
        if response:
            flag = 0 
            response[-1].alterpos = 0
            newResp = response.pop(-1)
            displace = 0
            while response:
                if newResp:
                    dist = newResp ^ response[flag]
                    dist = abs(dist.steps) + (abs(dist.octaves) * 7)
                    if dist < 5:
                        displace -= 1
                    elif dist == 5:
                        displace -= 0.2
                    newResp = False
                else:
                    displace -= 1
                response[flag].alterpos = displace * self.dictAlter[self.space]['displace']
                response.pop(flag)
                flag = not flag and -1 or 0
        for x in chord.content:
            x.alterDisplace = response and abs(displace) * self.dictAlter[self.space]['displace'] or 0
            if hasattr(x, 'alterpos'):
                x.alterpos += response and abs(displace) * self.dictAlter[self.space]['displace'] or 0

    def _create_neuma(self, beat, fig, note, direction=None):
        n = Neuma()
        if note.get_graph_duration()['dots']:
            n.text = 'S'
        n.width = fig.graph['width']
        if self.align == 'center':
            n.pos[0] = self.cursor + n.width/2 - 20
        else:
            if hasattr(note, 'alterDisplace'):
                n.pos[0] = self.cursor + note.alterDisplace + (note.displace * 18) + fig.displace
            else:
                n.pos[0] = self.cursor + (note.displace * 18)
        n.pos[1] = self.ids.central.pos[1] + (note.pos * self.space)
        self.add_widget(n)
        beat.neumas.append(n)
        self._aditional_lines(note, beat.neumas)
        self._accidentals(note, beat.neumas)
        if direction and not self.beamless:
            plica = direction[0] == 'up' and PlicaUp() or PlicaDown()
            if direction[0] == 'up':
                height = direction[1]['highest']
            elif direction[0] == 'down':
                height = direction[1]['lowest']
            dif = abs(height - note.pos)
            plica.pos = n.pos
            plica.height = self.space*(dif + 7)
            self.add_widget(plica)
            beat.neumas.append(plica)

    def _aditional_lines(self, note, beat):
        pos = note.pos
        if hasattr(note, 'alterDisplace'):
            alterDisplace = note.alterDisplace + (note.displace * 18) + note.displace
        else:
            alterDisplace = note.displace * 18
        if -6 < pos < 6:
            return
        direction = pos < 0 and -1 or 1
        pos = abs(pos)
        extralines = (pos - 4)//2 
        for line in range(extralines):
            l = AditionalLine(size=[self.space*4, self.ids.central.height])
            self.add_widget(l)
            l.pos = self.cursor - (l.width*0.15) + alterDisplace, self.ids.central.pos[1] + ((6+(line*2))* direction * self.space)
            beat.append(l)

    def _accidentals(self, note, beat):
        if not note.alter:
            return
        text = note.alter == -1 and 'b' or note.alter == -2 and 'B' or note.alter == 1 and 'n' or note.alter == 2 and 'N'
        key = note.alter < 0 and 'flat' or 'sharp'
        symbol = Alter(text=text)
        self.add_widget(symbol)
        symbol.size = self.dictAlter[self.space][key]['width'][abs(note.alter)], self.dictAlter[self.space][key]['height']
        if text == 'B':
            symbol.pos[0] = self.cursor - (self.space*3.6) + note.alterpos - note.displace
        else:
            symbol.pos[0] = self.cursor - (self.space*2.3) + note.alterpos - note.displace
        symbol.pos[1] = self.ids.central.pos[1] + (self.space * note.pos)
        beat.append(symbol)

    def _create_silence(self, beat, silence):
        n = Neuma(text=self.dict_silences[silence.duration]['str'])
        n.width = silence.graph['width']
        if self.align == 'center':
            n.pos[0] = self.cursor + n.width/2
        else:
            n.pos[0] = self.cursor
        n.pos[1] = self.ids.central.pos[1]-(4*self.space)
        n.valign = 'top'
        n.height = self.space * 9
        self.add_widget(n)
        n.text_size[1] = self.dict_silences[silence.duration]['height']
        beat.neumas.append(n)

    def _print_joiners_and_flags(self):
        for bar in self.content:
            for beat in bar.content:
                actualNotes = [x for x in beat.content if not isinstance(x, Silence)]
                if not actualNotes:
                    continue
                consecutive, independent = self.consecutiveShortNote(actualNotes)
                if independent:
                    self._print_flags(beat, independent)
                if consecutive:
                    self._print_joiners(beat, consecutive)

    def consecutiveShortNote(self, actualNotes):
        if len(actualNotes) < 2:
            return None, [(i, n) for i, n in enumerate(actualNotes)]
        shortNotes = [i for i, x in enumerate(actualNotes) if x.duration < 1]
        consecutive = [(note, shortNotes[i+1]) for i, note in enumerate(shortNotes[:-1]) if note + 1 == shortNotes[i+1]]
        consecutive = [note for note in {index for conj in consecutive for index in conj}]
        independent = [(note, actualNotes[note]) for note in shortNotes if not note in consecutive]
        consecutive = [(note, actualNotes[note]) for note in consecutive]
        return consecutive, independent

    def _print_flags(self, beat, actualNotes):
        plicas = [x for x in beat.neumas if isinstance(x, (PlicaDown, PlicaUp))]
        for i , x in actualNotes:
            if x.duration >= 1:
                continue
            n = Neuma()
            n.text = self.dictFlags[beat.beam_direction]['str'][x.duration]
            if beat.beam_direction == 'up':
                n.pos[0] = plicas[i].pos[0] + self.dictFlags['up']['pos_x'][self.space]
                n.pos[1] = plicas[i].pos[1] + plicas[i].height + self.dictFlags['up']['pos_y'][self.space]
            elif beat.beam_direction == 'down':
                n.pos[0] = plicas[i].pos[0] + self.dictFlags['down']['pos_x'][self.space]
                n.pos[1] = plicas[i].pos[1] - plicas[i].height + self.dictFlags['down']['pos_y'][self.space]
            n.valign = 'bottom'
            self.add_widget(n)
            beat.neumas.append(n)

            #if actu
        #for 
        #dictFlags

        pass

    def _print_joiners(self, beat, actualNotes):
        plicas = [x for x in beat.neumas if isinstance(x, (PlicaDown, PlicaUp))]
        subdis = ['join8ths', 'join16ths', 'join32ths', 'join64ths',  'join128ths']
        for i, x in actualNotes:
            if not hasattr(x, 'joiner'):
                x.joiner = ''

        lines = {x for x in subdis for i, note in actualNotes if x in note.joiner}
        if beat.silence_in_between:
            self._extend_plica(beat, len(lines))
        joiners_ = []
        for j, subdi in enumerate(subdis):
            for i, note in enumerate(actualNotes):
                note = note[1]
                if subdi not in note.joiner or note.joiner[subdi] == 'middle':
                    continue
                if note.joiner[subdi] in ['start', 'unique_start', 'unique_end']:
                    if beat.beam_direction == 'up':
                        joiners_.append(JoinerUp())
                        joiners_[-1].pos = plicas[i].pos[0], plicas[i].pos[1] + plicas[i].height - (self.space * j*1.5)
                    if beat.beam_direction == 'down':
                        joiners_.append(JoinerDown())
                        joiners_[-1].pos = plicas[i].pos[0], plicas[i].pos[1] - plicas[i].height + (self.space * j*1.5)
                    joiners_[-1].height = self.space
                elif note.joiner[subdi] == 'end':
                    joiners_[-1].width = plicas[i].pos[0] - joiners_[-1].pos[0]
                    self.add_widget(joiners_[-1])
                if note.joiner[subdi] == 'unique_start':
                    joiners_[-1].width = self.space * 2
                    self.add_widget(joiners_[-1])
                elif note.joiner[subdi] == 'unique_end':
                    joiners_[-1].width = self.space * 2 * -1
                    self.add_widget(joiners_[-1])
        if joiners_:
            beat.neumas.extend(joiners_)
    
    def _extend_plica(self, beat, subdis):
        for plica in [x for x in beat.neumas if isinstance(x, (PlicaUp, PlicaDown))]:
            if beat.beam_direction == 'up':
                if beat.silence_in_between and beat.border_notes['highest'] < -2:
                    plica.hieght += self.space * (abs(-2 - beat.border_notes['highest']))
                if subdis > 2:
                    plica.height += self.space * (subdis - 2)
            if beat.beam_direction == 'down':
                if beat.silence_in_between and beat.border_notes['lowest'] > 2:
                    plica.hieght += self.space * (abs(beat.border_notes['lowest'] - 2))
                if subdis > 2:
                    plica.height += self.space * (subdis - 2)


if __name__ == '__main__':
    
    class myApp(App):
        
        def build(self):
            rl = RelativeLayout()
            interStaff = InteractiveStaff()
            interStaff.init_staff()
            rl.add_widget(interStaff)
            return rl

    myApp().run()
