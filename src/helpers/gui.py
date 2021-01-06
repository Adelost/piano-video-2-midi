import os

import PySimpleGUI as sg
import json


class GUI:
    def __init__(self, layout,
                 default_args=None,
                 settings_file='settings.json',
                 save_settings_key=None,
                 ):
        self.settings_file = settings_file
        self.default_args = default_args
        self.save_settings_key = save_settings_key
        self.window = sg.Window('Piano video to midi', layout)
        self.window.finalize()
        self.load_args(default_args)

    def start(self, on_event):
        self.run_event_loop(on_event)

    def load_args(self, default_args):
        args = default_args
        saved_args = self.load_json(self.settings_file)
        if saved_args:
            args = saved_args
        self.remove_reserved_keys(args)
        for k, v in args.items():
            if k in self.window.key_dict:
                self.window[k].update(v)

    def remove_reserved_keys(self, args):
        invalid_keys = []
        for k in args:
            if k.startswith('Browse'):
                invalid_keys.append(k)
        for k in invalid_keys:
            del args[k]

    def save_settings(self, values):
        self.save_json(self.settings_file, values)

    def validate_args(self, args):
        invalid_keys = []
        if self.default_args:
            default_args = self.default_args
            for k, v in args.items():
                if k in default_args:
                    default_v = default_args[k]
                    try:
                        if isinstance(default_v, int):
                            v = int(float(v))
                        elif isinstance(default_v, float):
                            v = float(v)
                        elif isinstance(default_v, bool):
                            v = bool(v)

                    except ValueError:
                        if isinstance(default_v, int):
                            v = 0
                        if isinstance(default_v, float):
                            v = 0.0
                        if isinstance(default_v, bool):
                            v = False
                        pass
                    args[k] = v
                    self.window[k].update(v)
                else:
                    invalid_keys.append(k)
        for k in invalid_keys:
            # del args[k]
            pass

    def clear_settings(self):
        self.try_remove_file(self.settings_file)

    def try_remove_file(self, file_path):
        try:
            os.remove(file_path)
        except OSError:
            pass

    def save_json(self, file_path, data):
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load_json(self, file_path):
        try:
            f = open(file_path, encoding='utf-8')
            d = json.load(f)
            return d
        except FileNotFoundError:
            return None

    def is_file(self, file_path):
        return os.path.isfile(file_path)

    def is_folder(self, file_path):
        return os.path.isdir(file_path)

    def run_event_loop(self, on_event):
        while True:
            event, args = self.window.read()
            if self.window == sg.WIN_CLOSED:
                break
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
            self.validate_args(args)
            self.update_settings(args)
            on_event(event, args)
        pass

    def update_settings(self, args):
        if args[self.save_settings_key]:
            self.save_settings(args)
        else:
            self.clear_settings()
