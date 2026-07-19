from __future__ import annotations

from abip.scene.state import SceneObjectState, SceneState
from abip.tracking.tracks import FrameTracks


class SceneBuilder:
    def __init__(self, frame_width: int, frame_height: int) -> None:
        self.frame_width = frame_width
        self.frame_height = frame_height

    def build(self, frame_tracks: FrameTracks) -> SceneState:
        objects: list[SceneObjectState] = []
        pedestrian_count = 0
        vehicle_count = 0
        bicycle_count = 0
        notes: list[str] = []

        for track in frame_tracks.tracks:
            box = track.box
            center_x = (box.x1 + box.x2) / 2.0
            center_y = (box.y1 + box.y2) / 2.0

            horizontal_zone = self._horizontal_zone(center_x)
            proximity = self._proximity(box.y2)
            is_in_path = horizontal_zone == "center" and proximity in {"mid", "close"}

            objects.append(
                SceneObjectState(
                    track_id=track.track_id,
                    class_name=track.class_name,
                    center_x=center_x,
                    center_y=center_y,
                    horizontal_zone=horizontal_zone,
                    proximity=proximity,
                    is_in_path=is_in_path,
                )
            )

            if track.class_name == "person":
                pedestrian_count += 1
                if is_in_path:
                    notes.append("pedestrian near riding path")
            elif track.class_name == "car":
                vehicle_count += 1
                if is_in_path:
                    notes.append("vehicle ahead in path")
            elif track.class_name == "bicycle":
                bicycle_count += 1
                if is_in_path:
                    notes.append("bicycle near riding path")

        summary = self._build_summary(
            pedestrian_count=pedestrian_count,
            vehicle_count=vehicle_count,
            bicycle_count=bicycle_count,
            notes=notes,
        )

        return SceneState(
            frame_index=frame_tracks.frame_index,
            objects=objects,
            pedestrian_count=pedestrian_count,
            vehicle_count=vehicle_count,
            bicycle_count=bicycle_count,
            summary=summary,
        )

    def _horizontal_zone(self, center_x: float) -> str:
        third = self.frame_width / 3.0

        if center_x < third:
            return "left"
        if center_x < 2 * third:
            return "center"
        return "right"

    def _proximity(self, bottom_y: int) -> str:
        if bottom_y < self.frame_height * 0.45:
            return "far"
        if bottom_y < self.frame_height * 0.75:
            return "mid"
        return "close"

    def _build_summary(
        self,
        pedestrian_count: int,
        vehicle_count: int,
        bicycle_count: int,
        notes: list[str],
    ) -> str:
        parts: list[str] = []

        total_objects = pedestrian_count + vehicle_count + bicycle_count
        parts.append(f"{total_objects} relevant objects")

        if pedestrian_count:
            parts.append(f"{pedestrian_count} pedestrian(s)")
        if vehicle_count:
            parts.append(f"{vehicle_count} vehicle(s)")
        if bicycle_count:
            parts.append(f"{bicycle_count} bicycle(s)")

        if notes:
            parts.extend(notes)

        if not notes and total_objects == 0:
            return "scene clear"

        return "; ".join(parts)