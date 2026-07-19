from __future__ import annotations

from abip.planning.state import PlanState
from abip.risk.state import RiskState
from abip.scene.state import SceneState


class BehaviorPlanner:
    def plan(self, scene_state: SceneState, risk_state: RiskState) -> PlanState:
        reasons: list[str] = []
        maneuver = "continue"
        urgency = "low"

        objects = scene_state.objects
        in_path_objects = [obj for obj in objects if obj.is_in_path]

        if not objects:
            return PlanState(
                frame_index=scene_state.frame_index,
                maneuver="continue",
                urgency="low",
                reasons=["scene clear"],
            )

        if any(obj.horizontal_zone == "right" and obj.proximity in {"mid", "close"} for obj in objects):
            maneuver = "hold_line"
            urgency = "medium"
            reasons.append("right-side traffic nearby")

        if in_path_objects:
            priority_order = {"person": 0, "car": 1, "bicycle": 2}
            proximity_order = {"close": 0, "mid": 1, "far": 2}

            in_path_objects = sorted(
                in_path_objects,
                key=lambda obj: (
                    proximity_order.get(obj.proximity, 3),
                    priority_order.get(obj.class_name, 3),
                ),
            )

            nearest = in_path_objects[0]

            if nearest.class_name == "person":
                reasons.append(f"pedestrian in path (ID {nearest.track_id})")
                if nearest.horizontal_zone == "left":
                    maneuver = "steer_right"
                    urgency = "medium"
                elif nearest.horizontal_zone == "right":
                    maneuver = "steer_left"
                    urgency = "medium"
                else:
                    maneuver = "yield" if risk_state.score < 0.80 else "stop"
                    urgency = "high"

            elif nearest.class_name == "car":
                reasons.append(f"vehicle in path (ID {nearest.track_id})")
                if nearest.horizontal_zone == "left":
                    maneuver = "steer_right"
                    urgency = "medium"
                elif nearest.horizontal_zone == "right":
                    maneuver = "steer_left"
                    urgency = "medium"
                else:
                    maneuver = "yield" if risk_state.score < 0.85 else "stop"
                    urgency = "high"

            elif nearest.class_name == "bicycle":
                reasons.append(f"bicycle in path (ID {nearest.track_id})")
                if nearest.horizontal_zone == "left":
                    maneuver = "steer_right"
                    urgency = "medium"
                elif nearest.horizontal_zone == "right":
                    maneuver = "steer_left"
                    urgency = "medium"
                else:
                    maneuver = "slow_down"
                    urgency = "medium"

        else:
            if risk_state.score >= 0.60:
                maneuver = "slow_down"
                urgency = "medium"
                reasons.append("nearby objects ahead")
            elif risk_state.score < 0.20:
                maneuver = "continue"
                urgency = "low"
                reasons.append("scene appears clear")
            else:
                maneuver = "keep_right"
                urgency = "low"
                reasons.append("maintain curb-side position")

        return PlanState(
            frame_index=scene_state.frame_index,
            maneuver=maneuver,
            urgency=urgency,
            reasons=reasons,
        )