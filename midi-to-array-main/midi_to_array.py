from mido import MidiFile, MidiTrack, Message, MetaMessage, bpm2tempo
import click

class MusicMapping:
    '''
    Provide two mappings: name to int, int to name
    '''
    name_to_int = {}
    names = 'CDEFGAB'
    offsets = [0, 2, 4, 5, 7, 9, 11]
    start = 12
    base = 12
    for level in range(8):
        for n, offset in zip(names, offsets):
            name_to_int[n + str(level)] = start + level * base + offset
            name_to_int[n + '#' + str(level)] = name_to_int[n + str(level)] + 1
            name_to_int[n + 'b' + str(level)] = name_to_int[n + str(level)] - 1
    name_to_int['C8'] = 108
    name_to_int['R'] = -1

    int_to_name = {}
    for name, integer in name_to_int.items():
        if '#' not in name and 'b' not in name:
            int_to_name[integer] = name
    for name, integer in name_to_int.items():
        if 'b' not in name and int_to_name.get(integer) == None:
            int_to_name[integer] = name
    name_to_int[-1] = 'R'
class Note:
    def __init__(self, pitch, start_time) -> None:
        self.pitch = pitch
        self.start_time = start_time

    def __eq__(self, __o: object) -> bool:
        return self.pitch == __o.pitch

    def __lt__(self, other) -> bool:
        return self.pitch < other.pitch

    def get_rest(start_time):
        return Note(-1, start_time)

class Channel:
    def __init__(self) -> None:
        self.playing_notes = [Note.get_rest(0)]
        self.pitch = []
        self.duration = []

        self.prev_time = 0
        self.cur_time = 0
        self.note_on_buffer = []    # buffer notes arrive in the same time
        self.note_off_buffer = []

    def __len__(self):
        return len(self.pitch)

    def flush(self):
        '''
        Flush buffer.
        Log the highest note that is preempted / turned off.
        '''
        if self.playing_notes: # not empty
            high_pitch = max(self.playing_notes)

            if self.note_on_buffer:
                high_on = max(self.note_on_buffer)
            else:
                high_on = Note.get_rest(self.cur_time)

            if high_pitch < high_on or high_pitch in self.note_off_buffer:
                self.log_note(high_pitch)

        for note in self.note_off_buffer:
            self.playing_notes.remove(note)
        self.playing_notes += self.note_on_buffer
        self.note_on_buffer = []
        self.note_off_buffer = []

    def note_on(self, pitch, time):
        '''
        Turn on note [pitch] at global time [time].
        '''
        if time > self.cur_time:
            self.flush()
            self.cur_time = time
        self.note_on_buffer.append(Note(pitch, time))

    def note_off(self, pitch, time):
        if time > self.cur_time:
            self.flush()
            self.cur_time = time
        self.note_off_buffer.append(Note(pitch, time))

    def mute_all(self, time):
        self.flush()
        self.cur_time = time
            
        if self.playing_notes:
            high_pitch = max(self.playing_notes)
            self.log_note(high_pitch)
            self.playing_notes = [Note.get_rest(0)]

    def log_note(self, note: Note):
        if self.cur_time == self.prev_time:
            return
        
        self.pitch.append(note.pitch)
        self.duration.append(self.cur_time - self.prev_time)
        self.prev_time = self.cur_time
    

def midi_2_array(input, output, format, no_rest):
    mid = MidiFile(input)
    ticks_per_whole_note = mid.ticks_per_beat * 4
    # ticks_per_whole_note = 1
    tempo = None
    file_names = []

    for i, track in enumerate(mid.tracks):
        channels = [Channel() for k in range(16)]
        global_time = 0

        for msg in track:
            global_time += msg.time

            if tempo == None and msg.is_meta and msg.type == 'set_tempo':
                tempo = msg.tempo
            if not msg.is_meta:
                if msg.type == 'note_on' and msg.velocity > 0:
                    cid = msg.channel
                    channels[cid].note_on(msg.note, global_time)
                elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                    cid = msg.channel
                    channels[cid].note_off(msg.note, global_time)
                elif msg.type == 'reset':
                    for channel in channels:
                        channel.mute_all(global_time)
                elif msg.type == 'control_change' and msg.control == 123:
                    cid = msg.channel
                    channels[cid].mute_all(global_time)

        for j, channel in enumerate(channels):
            channel.flush()

            # remove rest
            if no_rest:
                pitch_res = []
                dura_res = []
                rest_len = 0
                while channel.pitch:
                    p = channel.pitch.pop()
                    d = channel.duration.pop()
                    if p == -1:
                        rest_len += d
                    else:
                        pitch_res.insert(0, p)
                        dura_res.insert(0, d + rest_len)
                        rest_len = 0
                channel.pitch = pitch_res
                channel.duration = dura_res

            if len(channel) > 1:
                file_names.append(output_array(channel, output, f'-track-{i}-channel{j}', format, ticks_per_whole_note, tempo))
    return file_names
    
def output_array(channel: Channel, dst, suffix, format, ticks_per_whole_note, tempo):
    result = ''
    if format == 'integer':
        result += ' '.join([str(p) for p in channel.pitch])
    elif format == 'name':
        result += ' '.join([MusicMapping.int_to_name[p] for p in channel.pitch])
    result += '\n'
    result += ' '.join([str(d / ticks_per_whole_note) for d in channel.duration])
    result += '\n'
    if tempo != None:
        result += str(tempo)

    with open(dst + suffix, 'w', encoding='utf-8') as fout:
        fout.write(result)
    
    return dst + suffix

def process_array_input(pitches, duration, format, ticks_per_whole_note):
    '''
    Caution: the start_time field in Note now stands for duration
    '''
    if format == 'integer':
        pitches = [int(p) for p in pitches]
    elif format == 'name':
        pitches = [MusicMapping.name_to_int[p] for p in pitches]
    duration = [round(float(d) * ticks_per_whole_note) for d in duration]
    return [Note(p, t) for p, t in zip(pitches, duration)]

def array_to_midi(input, output, format, bpm):
    mid = MidiFile()
    track = MidiTrack()
    mid.tracks.append(track)
    ticks_per_whole_note = mid.ticks_per_beat * 4

    with open(input, 'r') as fin:
        pitches = fin.readline().split()
        duration = fin.readline().split()
        notes = process_array_input(pitches, duration, format, ticks_per_whole_note)
        tempo = fin.readline().strip()

    if bpm != None:
        track.append(MetaMessage(type='set_tempo', tempo=bpm2tempo(bpm)))
    elif tempo:
        track.append(MetaMessage(type='set_tempo', tempo = int(tempo)))

    rest_time = 0
    for note in notes:
        if (note.pitch == -1):
            rest_time += note.start_time
        else:
            track.append(Message(
                'note_on', note=note.pitch, velocity=64, time=rest_time
            ))
            track.append(Message(
                'note_off', note=note.pitch, velocity=0, time=note.start_time
            ))
            rest_time = 0

    mid.save(output)

@click.command()
@click.option('--input', required=True, help='input file')
@click.option('--output', required=True, help='output file')
@click.option('--format', type=click.Choice(['name', 'integer'], case_sensitive=False),
                help="pitch format, note name (such as C4 D#5 Eb6) or integer (60 is C4)", default='name')
@click.option('--bpm', type=float, default=None, help='beats per minute')
@click.option('--no-rest', is_flag=True, default=False, help='If set, rests are removed by prolonging the previous note')
def convert(input, output, format, bpm, no_rest):
    if input.endswith('.mid') or input.endswith('.midi') or input.endswith('.MID') or input.endswith('.MIDI'):
        file_names = midi_2_array(input, output, format, no_rest)
        for file_name in file_names:
            array_to_midi(file_name, file_name + '.mid', format, bpm)
    else:
        array_to_midi(input, output, format, bpm)

if __name__ == '__main__':
    convert()