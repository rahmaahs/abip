from __future__ import annotations

from pathlib import Path

import cv2

from abip.ingestion.video_reader import VideoMetadata


class VideoWriter:
    def __init__(self, output_path: str | Path, metadata: VideoMetadata) -> None:
        self.output_path = Path(output_path)
        self.output_path.parent.mkdir(parents=True, exist_ok=True)

        self.metadata = metadata
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        fps = metadata.fps if metadata.fps > 0 else 30.0

        self._writer = cv2.VideoWriter(
            str(self.output_path),
            fourcc,
            fps,
            (metadata.width, metadata.height),
        )

        if not self._writer.isOpened():
            raise RuntimeError(f"Could not open video writer: {self.output_path}")

    def write(self, frame: object) -> None:
        self._writer.write(frame)

    def close(self) -> None:
        self._writer.release()

    def __enter__(self) -> "VideoWriter":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()