# Multiple Object Video Detection (HW 2, UCU AI 2026)

## Task

Predict bounding boxes and classes for every object in each frame of 48 unlabelled drone video clips (`test/images/`). There are 8 classes:

| id | class | id | class |
|----|-------|----|-------|
| 0 | person | 4 | truck |
| 1 | bicycle | 5 | tricycle |
| 2 | car | 6 | bus |
| 3 | van | 7 | motor |

The footage comes from the VisDrone2019-VID benchmark. Objects are small (often 10–30 px), dense and often occluded.

## Files

```
train/                  56 clips, 24,201 frames, labelled
val/                    7 clips, 2,846 frames, labelled
test/images/            48 clips, 3,811 frames, no labels
test_images.csv         list of test images and their sizes
sample_submission.csv   valid submission with empty predictions (scores 0)
```

`train/` and `val/` have the same layout:

```
images/<clip>/<frame>.jpg
labels/<clip>/<frame>.txt     YOLO labels
ignore/<clip>/<frame>.txt     ignored regions (only for frames that have them)
annotations_coco.json         the same labels in COCO format
data.yaml                     Ultralytics YOLO config; works with `yolo train data=train/data.yaml`
```

## Label formats

### YOLO (`labels/*.txt`)

One object per line: `class cx cy w h`. The box centre and size are normalised to 0–1 by image width and height. Class ids are 0–7 as in the table above.

```
0 0.328497 0.776455 0.026042 0.116402
```

### Ignored regions (`ignore/*.txt`)

One region per line: `cx cy w h`, normalised, with no class. These mark crowds, dense parking lots and other areas too small or too packed to annotate, plus VisDrone's "others" category. Detections there are not penalised in scoring. Treat these areas as "don't care" during training, for example by masking them out or by not counting detections there as background.

### COCO (`annotations_coco.json`)

Standard COCO with `bbox = [x, y, w, h]` in pixels, where `(x, y)` is the top-left corner.

- `category_id` is **1-based** (1 = person … 8 = motor), unlike the 0-based YOLO and submission ids.
- Ignored regions are annotations with `iscrowd = 1`.
- Extra annotation fields: `truncation`, `occlusion`, `track_id` (the same object across frames), `orig_category_id` (the original 10-class VisDrone id).
- `images` entries carry `video` and `frame_id`.

### `test_images.csv`

| column | meaning |
|--------|---------|
| `image_id` | row id for the submission, e.g. `clip_001_0000001` |
| `file_name` | path from the data root, e.g. `test/images/clip_001/0000001.jpg` |
| `clip` | clip name; one public/private leaderboard split per clip |
| `frame` | frame number within the clip, consecutive |
| `width`, `height` | image size in pixels |

Image sizes vary between clips (from 680×382 up to 1920×1080). Submit boxes in the pixel coordinates of each original image.

## Submission

One row per test image, in the format of `sample_submission.csv`:

```
image_id,PredictionString
clip_001_0000001,2 0.91 1366 580 26 44 0 0.55 809 625 29 66
clip_001_0000002,
```

`PredictionString` is a space-separated list of `class score x y width height` groups, where `(x, y)` is the top-left corner in pixels. This is **not** the normalised YOLO format. Leave it empty for an image with no detections. At most 500 detections per image are scored.
