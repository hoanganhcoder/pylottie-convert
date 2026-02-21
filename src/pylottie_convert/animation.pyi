from typing import Iterable, List, Optional, Tuple
import numpy as np
from numpy.typing import NDArray

RGBAFrame = NDArray[np.uint8]


class Animation:
    def __init__(self) -> None: ...

    # loaders
    def load_file(self, path: str) -> None: ...
    def load_json(self, data: str) -> None: ...
    def load_tgs(self, path: str) -> None: ...

    # metadata
    @property
    def width(self) -> int: ...
    @property
    def height(self) -> int: ...
    @property
    def size(self) -> Tuple[int, int]: ...
    @property
    def fps(self) -> float: ...
    @property
    def frames(self) -> int: ...
    @property
    def duration(self) -> float: ...

    # render
    def render(self, frame: int) -> RGBAFrame: ...
    def iter_frames(self) -> Iterable[RGBAFrame]: ...

    # export
    def save_gif(
        self,
        path: str,
        frames: Optional[List[RGBAFrame]] = ...,
        fps: Optional[float] = ...,
        loop: int = ...,
        disposal: int = ...,
        optimize: bool = ...,
    ) -> None: ...

    def save_webp(
        self,
        path: str,
        frames: Optional[List[RGBAFrame]] = ...,
        fps: Optional[float] = ...,
        loop: int = ...,
        quality: int = ...,
        method: int = ...,
        lossless: bool = ...,
    ) -> None: ...

    def save_apng(
        self,
        path: str,
        frames: Optional[List[RGBAFrame]] = ...,
        fps: Optional[float] = ...,
        loop: int = ...,
    ) -> None: ...