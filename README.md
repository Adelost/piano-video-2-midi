# piano-video-2-midi

Transcribes piano videos (e.g. Synthesia) to MIDI files by pixel variations in image.

![Video scanner GUI](./docs/images/gui-demo.png)

Result of video scan is saved in a custom JSON format. A MIDI-file is created by the second "JSON to MIDI"-GUI that allows additional
 customizations. 

![JSON GUI](./docs/images/json-gui-demo.png)

## Features

* Detects key presses through color variations in video
* Customizable detection (sensitivity, detect bright/dark color)
* Preview of video sampling
* Preview of MIDI file
* Allows modifying output MIDI, e.g. add sustain, transposing notes, auto transpose to C-major (to make song easier to play)

## Why?

Piano videos are popular on video sites such as Youtube, though often without any provided MIDI-file or piano sheet. 
A MIDI-file is often convenient as it can be played in programs such as [Synthesia](https://www.synthesiagame.com/) or imported into DAWs
 such as  [FL Studio](https://www.image-line.com/).
 
Programs to convert audio to MIDI-files exists, but most are not fully accurate. Transcribing the notes manually from the video is possible but time consuming. However, this is in many cases easily done with "piano-video-2-midi".
  
Besides it was fun to make, which should be reason enough for any software to exist.

## Prerequisites

* Python 3.7 (recommended)

Install dependencies with:

```
pip install -r requirements.txt
```


## Instructions

Run `video2json.py` followd by `json2midi.py` found in `src/`-directory.

```bash
python video2json.py
python json2midi.py
```

## Tips

* When previewing a video, hovering over the image will display your mouse's x and y coordinates relative to the image in the lower right
 corner. This helps you input the correct x,y values for the GUI.  
 
* A video file can be downloaded of Youtube-like sites in various ways. If you have Firefox one simple way is to install the [Easy Youtube
 Video Downloader Express](https://addons.mozilla.org/en-US/firefox/addon/easy-youtube-video-download/) or [Video DownloadHelper](https://addons.mozilla.org/en-US/firefox/addon/video-downloadhelper/).

* The program is not limited to Synthesia videos, but if you have any problems with key detection remember to try
 out different key activation thresholds and lot of videos should be possible to transcribe with a bit of experimentation.   

## Known problems

* Fast repeated keypresses of same key can in some cases be transcribed as one keypress. This happens if no frame in the video exists where
 the key is released in between key presses. 
 
## Alternatives

If this program did not fit your use case feel free to check out these
 alternatives:
 
  * Transcribes music to MIDI using a pretrained neural network in your browser with WebGL (not perfect but still quite impressive):
  https://piano-scribe.glitch.me/
 * An alternative video to MIDI transcriber:
 https://github.com/svsdval/video2midi
