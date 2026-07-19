from __future__ import annotations

from dataclasses import dataclass
from typing import List

from abip.scene.state import SceneState


@dataclass(frozen=True)
class CorridorState:
    frame_index: int
    corridor_zone: str
    corridor_clear: bool
    left_clear: bool
    right_clear: bool
    path_clear: bool
    corridor_pressure: str
    reasons: List[str]


class CorridorAnalyzer:
    def analyze(self, scene_state: SceneState) -> CorridorState:
        left_busy = False
        center_busy = False
        right_busy = False
        path_blocked = False
        reasons: list[str] = []

        for obj in scene_state.objects:
            if obj.horizontal_zone == "left" and obj.proximity in {"mid", "close"}:
                left_busy = True

            if obj.horizontal_zone == "center" and obj.proximity in {"mid", "close"}:
                center_busy = True

            if obj.horizontal_zone == "right" and obj.proximity in {"mid", "close"}:
                right_busy = True

            if obj.is_in_path:
                path_blocked = True
                reasons.append(f"{obj.class_name} in path (ID {obj.track_id})")

        corridor_zone = "right"
        corridor_clear = not right_busy and not path_blocked
        left_clear = not left_busy
        right_clear = not right_busy
        path_clear = not path_blocked

        busy_sides = sum([left_busy, center_busy, right_busy, path_blocked])
        if busy_sides == 0:
            corridor_pressure = "clear"
        elif busy_sides == 1:
            corridor_pressure = "light"
        elif busy_sides == 2:
            corridor_pressure = "moderate"
        else:
            corridor_pressure = "heavy"

        if corridor_clear:
            reasons.append("right-side riding corridor clear")
        elif right_busy:
            reasons.append("right-side corridor occupied")
        elif path_blocked:
            reasons.append("path occupied")

        return CorridorState(
            frame_index=scene_state.frame_index,
            corridor_zone=corridor_zone,
            corridor_clear=corridor_clear,
            left_clear=left_clear,
            right_clear=right_clear,
            path_clear=path_clear,
            corridor_pressure=corridor_pressure,
            reasons=reasons,
        )