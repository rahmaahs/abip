from __future__ import annotations

from abip.planning.free_space import FreeSpaceState
from abip.planning.state import PlanState
from abip.risk.state import RiskState
from abip.scene.state import SceneState


class BehaviorPlanner:
    def plan(
        self,
        scene_state: SceneState,
        risk_state: RiskState,
        free_space_state: FreeSpaceState,
    ) -> PlanState:
        reasons: list[str] = []
        maneuver = "continue"
        urgency = "low"

        in_path_objects = [obj for obj in scene_state.objects if obj.is_in_path]

        if not scene_state.objects:
            return PlanState(
                frame_index=scene_state.frame_index,
                maneuver="continue",
                urgency="low",
                reasons=["scene clear"],
            )

        if free_space_state.path_clear and free_space_state.right_open and risk_state.score < 0.30:
            maneuver = "keep_right"
            urgency = "low"
            reasons.append("right-side corridor clear")
            reasons.append("stay near curb line")

        elif in_path_objects:
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
            reasons.append(f"{nearest.class_name} in path (ID {nearest.track_id})")

            if free_space_state.right_open:
                maneuver = "steer_right"
                urgency = "medium"
                reasons.append("right-side space available")

            elif free_space_state.left_open:
                maneuver = "steer_left"
                urgency = "medium"
                reasons.append("left-side space available")

            else:
                maneuver = "yield" if risk_state.score < 0.80 else "stop"
                urgency = "high"
                reasons.append("no safe lateral space")

        else:
            if free_space_state.right_open and risk_state.score < 0.40:
                maneuver = "keep_right"
                urgency = "low"
                reasons.append("maintain curb-side position")
            elif risk_state.score >= 0.60:
                maneuver = "slow_down"
                urgency = "medium"
                reasons.append("traffic pressure near corridor")
            elif free_space_state.left_open and not free_space_state.right_open:
                maneuver = "hold_line"
                urgency = "low"
                reasons.append("right side pressured, hold line")
            else:
                maneuver = "continue"
                urgency = "low"
                reasons.append("scene appears clear")

        return PlanState(
            frame_index=scene_state.frame_index,
            maneuver=maneuver,
            urgency=urgency,
            reasons=reasons,
        )