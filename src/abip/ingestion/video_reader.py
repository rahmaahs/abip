from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator

import cv2


@dataclass(frozen=True)
class VideoMetadata:
    path: Path
    frame_count: int
    fps: float
    width: int
    height: int


class VideoReader:
    def __init__(self, video_path: str | Path) -> None:
        self.video_path = Path(video_path)

        if not self.video_path.exists():
            raise FileNotFoundError(f"Video not found: {self.video_path}")

        self._cap = cv2.VideoCapture(str(self.video_path))

        if not self._cap.isOpened():
            raise RuntimeError(f"Could not open video: {self.video_path}")

    def metadata(self) -> VideoMetadata:
        frame_count = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = float(self._cap.get(cv2.CAP_PROP_FPS))
        width = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        return VideoMetadata(
            path=self.video_path,
            frame_count=frame_count,
            fps=fps,
            width=width,
            height=height,
        )

    def frames(self) -> Iterator[tuple[int, object]]:
        index = 0

        while True:
            ok, frame = self._cap.read()
            if not ok:
                break

            yield index, frame
            index += 1

    def close(self) -> None:
        self._cap.release()

    def __enter__(self) -> "VideoReader":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()