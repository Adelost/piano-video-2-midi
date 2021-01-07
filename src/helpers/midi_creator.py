from midiutil.MidiFile import MIDIFile
import json

from helpers import utils


class MidiCreator:
    def __init__(self):
        self.START_TIME = 0.0
        self.ADD_SUSTAIN = False
        self.TRANSPOSE_C_MAJOR = False
        self.TRANSPOSE_SEMITONE = 0
        self.TRANSPOSE_OCTAVE = 0
        self.TEMPO = 120

    def get_default_args(self):
        return utils.get_attr_of_object(self)

    def create_midi(self, input_json, output_path, args):
        self._update_args(args)
        with open(input_json) as f:
            notes = json.load(f)
            notes = self._process_notes(notes)
            self._create_midi_from_notes(notes, output_path)

    def _update_args(self, args):
        utils.set_matching_attr_of_object(self, args)

    def _timeInSecToBeats(self, time):
        return time * self.TEMPO / 60

    def _create_midi_from_notes(self, notes, output_path):
        mf = MIDIFile(1)

        track = 0
        time = 0
        mf.addTrackName(track, time, "Main track")
        mf.addTempo(track, time, self.TEMPO)

        channel = 0
        volume = 100

        for note in notes:
            pitch, time, duration = note
            time = self._timeInSecToBeats(time)
            duration = self._timeInSecToBeats(duration)
            mf.addNote(track, channel, pitch, time, duration, volume)

        with open(output_path, 'wb') as f:
            mf.writeFile(f)

    def _process_notes(self, notes):
        out = []
        prev_notes_map = {}

        if self.TRANSPOSE_C_MAJOR:
            self._transpose_to_c_major(notes)

        for note in notes:
            note[1] -= self.START_TIME
            if note[1] < 0:
                continue
            note[0] += self.TRANSPOSE_SEMITONE
            note[0] += 12 * self.TRANSPOSE_OCTAVE
            if note[0] < 0:
                continue
            pitch, time, duration = note
            if self.ADD_SUSTAIN:
                if pitch in prev_notes_map:
                    sustain = time - prev_notes_map[pitch][1]
                    prev_notes_map[pitch][2] = sustain
            prev_notes_map[pitch] = note
            out.append(note)
        return out

    def _transpose_to_c_major(self, notes):
        note_count = [0] * 12
        for note in notes:
            note_type = note[0] % 12
            note_count[note_type] += 1
        max_hits = 0
        max_hits_offset = 0
        for i in range(12):
            hits = 0
            hits += note_count[(0 + i) % 12]
            hits += note_count[(2 + i) % 12]
            hits += note_count[(4 + i) % 12]
            hits += note_count[(5 + i) % 12]
            hits += note_count[(7 + i) % 12]
            hits += note_count[(9 + i) % 12]
            hits += note_count[(11 + i) % 12]
            if hits > max_hits:
                max_hits = hits
                max_hits_offset = i
        if max_hits_offset > 6:
            max_hits_offset -= 12
        for note in notes:
            note[0] -= max_hits_offset
