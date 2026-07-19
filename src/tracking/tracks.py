from __future__ import annotations

from dataclasses import dataclass
from typing import List

from abip.perception.detections import BoundingBox


@dataclass(frozen=True)
class TrackedObject:
    track_id: int
    class_name: str
    confidence: float
    box: BoundingBox


@dataclass(frozen=True)
class FrameTracks:
    frame_index: int
    tracks: List[TrackedObject]