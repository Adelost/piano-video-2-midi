import PySimpleGUI as sg
import matplotlib.pyplot as plt

from helpers.gui import GUI
from helpers.video_scanner import VideoScanner

layout = [
    [sg.Checkbox('Remember settings next startup', key='SAVE_SETTINGS', enable_events=True)],

    [sg.Text('Input video'), sg.Input(key='INPUT_FILE'), sg.FileBrowse(file_types=(("Video file", "*.mp4"),))],
    [sg.Text('Output folder'), sg.Input(key='OUTPUT_FOLDER'), sg.FolderBrowse()],

    [sg.Frame(title='Keys', layout=[
        [sg.Text('White start X-cord'), sg.Input(size=(10, 1), key='KEY_WHITE_X')],
        [sg.Text('White Y-cord'), sg.Input(size=(10, 1), key='KEY_WHITE_Y')],
        [sg.Text('Black Y-cord'), sg.Input(size=(10, 1), key='KEY_BLACK_Y')],
    ]), sg.Frame(title='Octave', layout=[
        [sg.Text('First end X-cord'), sg.Input(size=(10, 1), key='OCTAVE_FIRST_END_X')],
        [sg.Text('Start C-note (1 for C1, 2 for C2)'), sg.Input(size=(10, 1), key='OCTAVE_START')],
        [sg.Text('Count'), sg.Input(size=(10, 1), key='OCTAVE_COUNT')],
    ])],

    [sg.Frame(title='White key activation', layout=[
        [sg.Text('Threshold'), sg.Input(size=(10, 1), key='KEY_WHITE_ACTIVATION')],
        [sg.Checkbox('Detect white color (else black)', key='KEY_WHITE_DETECT_WHITE')],
    ]), sg.Frame(title='Black key activation', layout=[
        [sg.Text('Threshold'), sg.Input(size=(10, 1), key='KEY_BLACK_ACTIVATION')],
        [sg.Checkbox('Detect white color (else black)', key='KEY_BLACK_DETECT_WHITE')],
    ])],

    [sg.Frame(title='Sample', layout=[
        [sg.Text('Radius'), sg.Input(size=(10, 1), key='SAMPLE_RADIUS')],
    ])],

    [sg.Frame(title='Black key offsets', layout=[
        [
            sg.Text('1 (C#)'), sg.Input(size=(10, 1), key='KEY_BLACK_OFFSET_1'),
            sg.Text('2 (D#)'), sg.Input(size=(10, 1), key='KEY_BLACK_OFFSET_2')
        ],
        [
            sg.Text('3 (F#)'), sg.Input(size=(10, 1), key='KEY_BLACK_OFFSET_3'),
            sg.Text('4 (G#)'), sg.Input(size=(10, 1), key='KEY_BLACK_OFFSET_4'),
            sg.Text('5 (A#)'), sg.Input(size=(10, 1), key='KEY_BLACK_OFFSET_5')
        ],
    ])],

    [sg.Frame(title='Time', layout=[
        [sg.Text('Start'), sg.Input(size=(10, 1), key='START_TIME')],
        [sg.Text('End'), sg.Input(size=(10, 1), key='END_TIME')],
        [sg.Text('Preview step size (frames)'), sg.Input(size=(10, 1), key='PREVIEW_STEP_SIZE')],
    ])],

    [sg.Button('Preview', key='PREVIEW'), sg.Button('Preview Step', key='PREVIEW_STEP')],
    [sg.Button('Process', key='START')],
]


def on_preview_image(image):
    plt.imshow(image)
    plt.show()


def on_progress(count, max_count):
    sg.one_line_progress_meter('Progress', count, max_count)


process = VideoScanner(on_preview_image=on_preview_image, on_progress=on_progress)
default_args = process.get_default_args()
gui = GUI(
    layout,
    title='Video to JSON',
    default_args=default_args,
    save_settings_key='SAVE_SETTINGS',
    settings_file='video2json.settings.json')


def validate_args(args):
    if not gui.is_file(args['INPUT_FILE']):
        sg.popup('No input video selected')
        return False
    if not gui.is_folder(args['OUTPUT_FOLDER']):
        sg.popup('No output folder selected')
        return False
    return True


def on_event(event, args):
    if event == 'START':
        if validate_args(args):
            process.start(args)
    if event == 'PREVIEW':
        if validate_args(args):
            process.start(args, preview=True)
    if event == 'PREVIEW_STEP':
        if validate_args(args):
            process.preview_step(args)
    pass


gui.start(on_event)
