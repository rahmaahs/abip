from __future__ import annotations

from dataclasses import dataclass
from typing import List

from abip.scene.state import SceneState


@dataclass(frozen=True)
class FreeSpaceState:
    frame_index: int
    left_pressure: float
    center_pressure: float
    right_pressure: float
    left_open: bool
    center_open: bool
    right_open: bool
    preferred_side: str
    path_clear: bool
    reasons: List[str]


class FreeSpaceEstimator:
    def analyze(self, scene_state: SceneState) -> FreeSpaceState:
        left_pressure = 0.0
        center_pressure = 0.0
        right_pressure = 0.0
        reasons: list[str] = []

        class_weight_map = {
            "person": 1.0,
            "car": 1.3,
            "bicycle": 0.8,
        }
        proximity_weight_map = {
            "far": 0.4,
            "mid": 0.8,
            "close": 1.2,
        }

        for obj in scene_state.objects:
            class_weight = class_weight_map.get(obj.class_name, 0.7)
            proximity_weight = proximity_weight_map.get(obj.proximity, 0.6)
            weight = class_weight * proximity_weight

            if obj.horizontal_zone == "left":
                left_pressure += weight
            elif obj.horizontal_zone == "center":
                center_pressure += weight
            else:
                right_pressure += weight

            if obj.is_in_path:
                center_pressure += weight * 0.8
                reasons.append(f"{obj.class_name} in path (ID {obj.track_id})")

        left_open = left_pressure < 1.5
        center_open = center_pressure < 1.2
        right_open = right_pressure < 1.3
        path_clear = not any(obj.is_in_path for obj in scene_state.objects)

        if right_open:
            preferred_side = "right"
        elif left_open:
            preferred_side = "left"
        elif center_open:
            preferred_side = "center"
        else:
            preferred_side = "blocked"

        if path_clear and right_open:
            reasons.append("right-side riding corridor open")
        elif not path_clear:
            reasons.append("path occupied")
        elif not right_open:
            reasons.append("right-side corridor pressured")

        return FreeSpaceState(
            frame_index=scene_state.frame_index,
            left_pressure=left_pressure,
            center_pressure=center_pressure,
            right_pressure=right_pressure,
            left_open=left_open,
            center_open=center_open,
            right_open=right_open,
            preferred_side=preferred_side,
            path_clear=path_clear,
            reasons=reasons,
        )