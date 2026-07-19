from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from abip.perception.detections import BoundingBox, Detection, FrameDetections


@dataclass
class FakeDetector:
    """
    Temporary detector used to test the pipeline before YOLO is added.

    This does not perform real computer vision.
    It returns a few synthetic detections so the rest of the system can
    already work with detection-shaped data.
    """

    def detect(self, frame_index: int, frame: Any) -> FrameDetections:
        height, width = frame.shape[:2]

        # Create a few moving boxes so the output looks dynamic.
        shift = (frame_index * 5) % 80

        detections = [
            Detection(
                class_name="person",
                confidence=0.91,
                box=BoundingBox(
                    x1=max(0, 120 + shift),
                    y1=max(0, height // 2 - 120),
                    x2=max(0, 220 + shift),
                    y2=max(0, height // 2 + 40),
                ),
            ),
            Detection(
                class_name="car",
                confidence=0.87,
                box=BoundingBox(
                    x1=max(0, width - 420 - shift),
                    y1=max(0, height // 2 - 180),
                    x2=max(0, width - 180 - shift),
                    y2=max(0, height // 2 + 20),
                ),
            ),
            Detection(
                class_name="bicycle",
                confidence=0.79,
                box=BoundingBox(
                    x1=max(0, width // 2 - 80),
                    y1=max(0, height // 2 + 40),
                    x2=max(0, width // 2 + 80),
                    y2=max(0, height // 2 + 180),
                ),
            ),
        ]

        return FrameDetections(
            frame_index=frame_index,
            detections=detections,
        )