from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class SceneObjectState:
    track_id: int
    class_name: str
    center_x: float
    center_y: float
    horizontal_zone: str
    proximity: str
    is_in_path: bool


@dataclass(frozen=True)
class SceneState:
    frame_index: int
    objects: List[SceneObjectState]
    pedestrian_count: int
    vehicle_count: int
    bicycle_count: int
    summary: str