from typing import Iterable, List, Optional
from numpy.typing import NDArray
import numpy as np
import os

RGBAFrame = NDArray[np.uint8]


class Animation:
    def __init__(self):
        from ._pylottie import LottieEngine
        self._eng = LottieEngine()

    # -------------------------
    # LOADERS
    # -------------------------

    def load_file(self, path: str) -> None:
        if not self._eng.load_from_file(path):
            raise RuntimeError(f"Failed to load file: {path}")

    def load_json(self, data: str) -> None:
        if not self._eng.load_from_data(data):
            raise RuntimeError("Invalid JSON")

    def load_tgs(self, path: str) -> None:
        import gzip

        with gzip.open(path, "rb") as f:
            raw = f.read()

        if not self._eng.load_from_data(raw.decode("utf-8")):
            raise RuntimeError("Invalid TGS")

    # -------------------------
    # METADATA
    # -------------------------

    @property
    def width(self) -> int:
        return self._eng.width()

    @property
    def height(self) -> int:
        return self._eng.height()

    @property
    def size(self) -> tuple[int, int]:
        return self.width, self.height

    @property
    def fps(self) -> float:
        return self._eng.frame_rate()

    @property
    def frames(self) -> int:
        return self._eng.total_frames()

    @property
    def duration(self) -> float:
        return self._eng.duration()

    # -------------------------
    # RENDER
    # -------------------------

    def render(self, frame: int) -> RGBAFrame:
        w, h = self.size

        if w <= 0 or h <= 0:
            raise RuntimeError("Animation not loaded")

        return self._eng.render_rgba(frame, w, h)

    def iter_frames(self) -> Iterable[RGBAFrame]:
        total = self.frames

        if total <= 0:
            raise RuntimeError("Animation has no frames")

        for i in range(total):
            yield self.render(i)

    # -------------------------
    # INTERNAL
    # -------------------------

    def _duration_ms(self, fps: Optional[float]) -> int:
        fps = fps or self.fps
        if fps <= 0:
            raise RuntimeError("Invalid FPS")
        return int(1000 / fps)

    def _pil_frames(self, frames: Optional[List[RGBAFrame]]):
        from PIL import Image

        frames = frames or list(self.iter_frames())

        if not frames:
            raise RuntimeError("No frames")

        return [Image.fromarray(f, "RGBA") for f in frames]

    # -------------------------
    # GIF (requires Pillow)
    # -------------------------

    def save_gif(
        self,
        path: str,
        frames: Optional[List[RGBAFrame]] = None,
        fps: Optional[float] = None,
        loop: int = 0,
        disposal: int = 2,
        optimize: bool = False,
    ) -> None:
        from PIL import Image

        pil_frames = self._pil_frames(frames)
        duration_ms = self._duration_ms(fps)

        pil_frames[0].save(
            path,
            save_all=True,
            append_images=pil_frames[1:],
            duration=duration_ms,
            loop=loop,
            disposal=disposal,
            optimize=optimize,
        )

        if not os.path.exists(path):
            raise RuntimeError("GIF not written")

    # -------------------------
    # WebP (requires Pillow)
    # -------------------------

    def save_webp(
        self,
        path: str,
        frames: Optional[List[RGBAFrame]] = None,
        fps: Optional[float] = None,
        loop: int = 0,
        quality: int = 90,
        method: int = 4,
        lossless: bool = False,
    ) -> None:
        from PIL import Image

        pil_frames = self._pil_frames(frames)
        duration_ms = self._duration_ms(fps)

        pil_frames[0].save(
            path,
            save_all=True,
            append_images=pil_frames[1:],
            duration=duration_ms,
            loop=loop,
            format="WEBP",
            quality=quality,
            method=method,
            lossless=lossless,
        )

        if not os.path.exists(path):
            raise RuntimeError("WebP not written")

    # -------------------------
    # APNG (requires Pillow)
    # -------------------------

    def save_apng(
        self,
        path: str,
        frames: Optional[List[RGBAFrame]] = None,
        fps: Optional[float] = None,
        loop: int = 0,
    ) -> None:
        from PIL import Image

        pil_frames = self._pil_frames(frames)
        duration_ms = self._duration_ms(fps)

        pil_frames[0].save(
            path,
            save_all=True,
            append_images=pil_frames[1:],
            duration=duration_ms,
            loop=loop,
            disposal=1,
            blend=0,
            format="PNG",
        )

        if not os.path.exists(path):
            raise RuntimeError("APNG not written")