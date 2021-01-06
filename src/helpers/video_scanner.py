import os
from pathlib import Path

import cv2
import json

from src.helpers import utils


class VideoScanner:
    def __init__(self,
                 on_preview_image=None,
                 on_progress=None
                 ):
        self.on_progress = on_progress
        self.on_preview_image = on_preview_image

        self.tracked_keys = {}
        self.curr_time = 0
        self.notes = []
        self.preview = False
        self.cap = None

        self.INPUT_FILE = ''

        self.KEY_WHITE_X = 32
        self.KEY_WHITE_Y = 300
        self.KEY_BLACK_Y = 270

        self.OCTAVE_FIRST_END_X = 186.0
        self.OCTAVE_START = 1
        self.OCTAVE_COUNT = 4

        self.SAMPLE_RADIUS = 3
        self.KEY_WHITE_ACTIVATION = 0.3
        self.KEY_WHITE_DETECT_WHITE = False
        self.KEY_BLACK_ACTIVATION = 0.3
        self.KEY_BLACK_DETECT_WHITE = True

        self.KEY_BLACK_OFFSET_1 = 0.4
        self.KEY_BLACK_OFFSET_2 = 0.6
        self.KEY_BLACK_OFFSET_3 = 0.37
        self.KEY_BLACK_OFFSET_4 = 0.5
        self.KEY_BLACK_OFFSET_5 = 0.63

        self.START_TIME = 1.0
        self.END_TIME = 999.0
        self.PREVIEW_STEP_SIZE = 10

    def get_default_args(self):
        return utils.get_attr_of_object(self)

    def start(self, args, preview=False):
        self._update_args(args)
        if self.cap:
            self._stop_capture()
        self.preview = preview
        self.notes = []
        self.tracked_keys = {}
        self._process_video()
        if not preview:
            self._save_notes()

    def preview_step(self, args):
        self._update_args(args)
        if not self.cap:
            self.start(args, preview=True)
            return
        image = None
        for i in range(self.PREVIEW_STEP_SIZE):
            success, image = self.cap.read()
            if not success:
                self._stop_capture()
                return
        self._track_notes(image)
        self._preview_image(image)

    def _preview_image(self, image):
        if self.on_preview_image:
            self.on_preview_image(image)

    def _stop_capture(self):
        self.cap.release()
        self.cap = None

    def _update_args(self, args):
        utils.set_matching_attr_of_object(self, args)

    def _process_video(self):
        self.cap = cv2.VideoCapture(self.INPUT_FILE)
        success, image = self.cap.read()
        count = 0
        max_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        video_curr_time = 0
        progress_intervall = 60
        while success and video_curr_time < self.END_TIME:
            success, image = self.cap.read()
            video_curr_time = self.cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
            self.curr_time = video_curr_time - self.START_TIME
            if video_curr_time >= self.START_TIME:
                self._track_notes(image)
                if self.preview:
                    self._preview_image(image)
                    return
                if count % progress_intervall == 0:
                    if self.on_progress:
                        self.on_progress(count, max_count)
            count += 1
        self.on_progress(max_count, max_count)
        self._stop_capture()

    def _track_notes(self, image):
        octave_width = self.OCTAVE_FIRST_END_X - self.KEY_WHITE_X
        key_width = octave_width / 7
        for i in range(self.OCTAVE_COUNT):
            x = self.KEY_WHITE_X + octave_width * i
            offset = (self.OCTAVE_START + i) * 12 + 12
            self._track_note(0 + offset, image, x + key_width * 0)
            self._track_note(1 + offset, image, x + key_width * (0 + self.KEY_BLACK_OFFSET_1), black=True)
            self._track_note(2 + offset, image, x + key_width * 1)
            self._track_note(3 + offset, image, x + key_width * (1 + self.KEY_BLACK_OFFSET_2), black=True)
            self._track_note(4 + offset, image, x + key_width * 2)
            self._track_note(5 + offset, image, x + key_width * 3)
            self._track_note(6 + offset, image, x + key_width * (3 + self.KEY_BLACK_OFFSET_3), black=True)
            self._track_note(7 + offset, image, x + key_width * 4)
            self._track_note(8 + offset, image, x + key_width * (4 + self.KEY_BLACK_OFFSET_4), black=True)
            self._track_note(9 + offset, image, x + key_width * 5)
            self._track_note(10 + offset, image, x + key_width * (5 + self.KEY_BLACK_OFFSET_5), black=True)
            self._track_note(11 + offset, image, x + key_width * 6)

    pass

    def _track_note(self, note_id, image, x, black=False):
        y = self.KEY_WHITE_Y
        if black:
            y = self.KEY_BLACK_Y
        x = round(x)
        y = round(y)
        sample = image[y - self.SAMPLE_RADIUS: y + self.SAMPLE_RADIUS, x - self.SAMPLE_RADIUS: x + self.SAMPLE_RADIUS]
        whiteness = sample.mean(axis=0).mean(axis=0).mean(axis=0) / 255
        blackness = 1 - whiteness
        is_pressed = False
        if black:
            if self.KEY_BLACK_DETECT_WHITE:
                is_pressed = whiteness > self.KEY_BLACK_ACTIVATION
            else:
                is_pressed = blackness > self.KEY_BLACK_ACTIVATION
        if not black:
            if self.KEY_WHITE_DETECT_WHITE:
                is_pressed = whiteness > self.KEY_WHITE_ACTIVATION
            else:
                is_pressed = blackness > self.KEY_WHITE_ACTIVATION

        # is_pressed = black and activation > self.KEY_BLACK_ACTIVATION or not black and activation < self.KEY_WHITE_ACTIVATION
        is_tracked = note_id in self.tracked_keys
        if is_pressed:
            if not is_tracked:
                self.tracked_keys[note_id] = self.curr_time
        else:
            if is_tracked:
                start_time = self.tracked_keys[note_id]
                duration = self.curr_time - start_time
                note = (note_id, start_time, duration)
                self.notes.append(note)
                del self.tracked_keys[note_id]

        if self.preview:
            if is_pressed:
                image[y - self.SAMPLE_RADIUS: y + self.SAMPLE_RADIUS, x - self.SAMPLE_RADIUS: x + self.SAMPLE_RADIUS] = (0, 255, 0)
            else:
                image[y - self.SAMPLE_RADIUS: y + self.SAMPLE_RADIUS, x - self.SAMPLE_RADIUS: x + self.SAMPLE_RADIUS] = (255, 0, 0)

    def _save_notes(self):
        self.notes.sort(key=lambda x: x[1])
        input_path = Path(self.INPUT_FILE)
        output_dir = input_path.parent
        file_name = input_path.stem + '.json'
        output_path = os.path.join(output_dir, file_name)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)
        pass
