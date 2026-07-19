from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class BoundingBox:
    x1: int
    y1: int
    x2: int
    y2: int


@dataclass(frozen=True)
class Detection:
    class_name: str
    confidence: float
    box: BoundingBox


@dataclass(frozen=True)
class FrameDetections:
    frame_index: int
    detections: List[Detection]