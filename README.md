# PyLottie-Convert

High performance Lottie renderer powered by `rlottie`.

`pylottie-convert` lets you load Lottie (`.json` / `.tgs`) animations and export them to image formats like GIF, WebP, and APNG.

## Installation

Install from PyPI:

```bash
pip install pylottie-convert
```

If you want export features (GIF / WebP / APNG), install Pillow too:

```bash
pip install "pylottie-convert[all]"
```

Or install specific extras:

```bash
pip install "pylottie-convert[gif]"
pip install "pylottie-convert[webp]"
pip install "pylottie-convert[apng]"
```

## Requirements

- Python `>= 3.9`
- `numpy`
- `pillow` (optional, required for `save_gif`, `save_webp`, `save_apng`)

## Quick Start

### 1) Load from `.json` and inspect metadata

```python
from pylottie_convert import Animation

anim = Animation()
anim.load_file("assets/sample.json")

print("Size:", anim.size)       # (width, height)
print("FPS:", anim.fps)
print("Frames:", anim.frames)
print("Duration:", anim.duration)
```

### 2) Render a frame to NumPy RGBA array

```python
frame0 = anim.render(0)
print(frame0.shape, frame0.dtype)  # (H, W, 4) uint8
```

### 3) Export animation

```python
# GIF
anim.save_gif("out.gif", fps=anim.fps)

# Animated WebP
anim.save_webp("out.webp", fps=anim.fps, quality=90)

# APNG
anim.save_apng("out.png", fps=anim.fps)
```

### 4) Load Telegram `.tgs` and export

```python
from pylottie_convert import Animation

anim = Animation()
anim.load_tgs("assets/telegram_sticker.tgs")

print("TGS size:", anim.size)
print("TGS fps:", anim.fps)

# Export to GIF/WebP
anim.save_gif("telegram_sticker.gif", fps=anim.fps)
anim.save_webp("telegram_sticker.webp", fps=anim.fps, quality=90)
```

## Load from JSON string

```python
from pathlib import Path
from pylottie_convert import Animation

data = Path("assets/sample.json").read_text(encoding="utf-8")

anim = Animation()
anim.load_json(data)
anim.save_gif("from_json.gif")
```

## Load from Telegram `.tgs`

```python
from pylottie_convert import Animation

anim = Animation()
anim.load_tgs("assets/sticker.tgs")
anim.save_webp("sticker.webp")
```

## API Overview

Main class: `Animation`

- Loaders:
	- `load_file(path)`
	- `load_json(data)`
	- `load_tgs(path)`
- Metadata:
	- `width`, `height`, `size`, `fps`, `frames`, `duration`
- Rendering:
	- `render(frame)` -> `numpy.ndarray` (`RGBA`, `uint8`)
	- `iter_frames()`
- Export (requires Pillow):
	- `save_gif(path, fps=None, loop=0, disposal=2, optimize=False)`
	- `save_webp(path, fps=None, loop=0, quality=90, method=4, lossless=False)`
	- `save_apng(path, fps=None, loop=0)`

## Notes

- Ensure the input file is a valid Lottie JSON or valid `.tgs` file.
- Export methods raise `RuntimeError` if writing output fails.

## License

MIT

