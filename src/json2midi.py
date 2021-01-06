import os
from pathlib import Path

import PySimpleGUI as sg

from src.helpers import media
from src.helpers.gui import GUI
from src.helpers.midi_creator import MidiCreator

layout = [
    [sg.Checkbox('Remember settings next startup', key='SAVE_SETTINGS', enable_events=True)],
    [sg.Text('Input JSON'), sg.Input(key='INPUT_FILE'), sg.FileBrowse(file_types=(("JSON file", "*.json"),))],
    [sg.Text('Output folder'), sg.Input(key='OUTPUT_FOLDER'), sg.FolderBrowse()],
    [sg.Text('Transpose semitone'), sg.Input(size=(10, 1), key='TRANSPOSE_SEMITONE'),
     sg.Text('Transpose octave'), sg.Input(size=(10, 1), key='TRANSPOSE_OCTAVE')],
    [sg.Checkbox('Add sustain', key='ADD_SUSTAIN'), sg.Checkbox('Transpose to C Major', key='TRANSPOSE_C_MAJOR')],
    [sg.Text('Start time'), sg.Input(size=(10, 1), key='START_TIME'), sg.Text('Tempo (BPM)'), sg.Input(size=(10, 1), key='TEMPO')],
    [sg.Button('Play', key='PLAY'), sg.Button('Pause/Unpause', key='PAUSE'), sg.Button('Stop', key='STOP')],
    [sg.Button('Create', key='CREATE')],
]

midi_creator = MidiCreator()
default_args = midi_creator.get_default_args()
gui = GUI(
    layout,
    title='JSON to MIDI',
    default_args=default_args,
    save_settings_key='SAVE_SETTINGS',
    settings_file='json2midi.settings.json')


def validate_args(args):
    if not gui.is_file(args['INPUT_FILE']):
        sg.popup('No input JSON selected')
        return False
    if not gui.is_folder(args['OUTPUT_FOLDER']):
        sg.popup('No output folder selected')
        return False
    return True


def get_output_file_path(args):
    input_path = Path(args['INPUT_FILE'])
    output_dir = args['OUTPUT_FOLDER']
    file_name = input_path.stem + '.mid'
    output_path = os.path.join(output_dir, file_name)
    return output_path


def on_event(event, args):
    if event == 'PLAY':
        if validate_args(args):
            output_path = get_output_file_path(args)
            midi_creator.create_midi(args['INPUT_FILE'], output_path, args)
            media.play_midi(output_path)
    if event == 'STOP':
        if validate_args(args):
            media.stop_midi()
    if event == 'PAUSE':
        if validate_args(args):
            media.pause_midi()
    if event == 'CREATE':
        if validate_args(args):
            output_path = get_output_file_path(args)
            midi_creator.create_midi(args['INPUT_FILE'], output_path, args)
            sg.popup('Saved to ' + output_path)
    pass


gui.start(on_event)
