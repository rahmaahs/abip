from __future__ import annotations

from abip.planning.corridor import CorridorState
from abip.planning.state import PlanState
from abip.risk.state import RiskState
from abip.scene.state import SceneState


class BehaviorPlanner:
    def plan(
        self,
        scene_state: SceneState,
        risk_state: RiskState,
        corridor_state: CorridorState,
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

        if corridor_state.corridor_clear and not in_path_objects and risk_state.score < 0.30:
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

            if nearest.class_name == "person":
                reasons.append(f"pedestrian in path (ID {nearest.track_id})")
                if corridor_state.left_clear:
                    maneuver = "steer_left"
                    urgency = "medium"
                    reasons.append("left side open for avoidance")
                else:
                    maneuver = "yield" if risk_state.score < 0.80 else "stop"
                    urgency = "high"
                    reasons.append("no safe lateral space")

            elif nearest.class_name == "car":
                reasons.append(f"vehicle in path (ID {nearest.track_id})")
                if corridor_state.left_clear:
                    maneuver = "steer_left"
                    urgency = "medium"
                    reasons.append("left side open for avoidance")
                else:
                    maneuver = "yield" if risk_state.score < 0.85 else "stop"
                    urgency = "high"
                    reasons.append("no safe lateral space")

            elif nearest.class_name == "bicycle":
                reasons.append(f"bicycle in path (ID {nearest.track_id})")
                if corridor_state.left_clear:
                    maneuver = "steer_left"
                    urgency = "medium"
                    reasons.append("passing around bicycle on left")
                else:
                    maneuver = "slow_down"
                    urgency = "medium"
                    reasons.append("left side not clear")

        else:
            if corridor_state.corridor_pressure == "heavy":
                maneuver = "slow_down"
                urgency = "medium"
                reasons.append("heavy traffic pressure near corridor")
            elif risk_state.score < 0.20:
                maneuver = "continue"
                urgency = "low"
                reasons.append("scene appears clear")
            else:
                maneuver = "keep_right"
                urgency = "low"
                reasons.append("maintain curb-side position")

        if corridor_state.right_clear and maneuver == "continue" and risk_state.score < 0.35:
            maneuver = "keep_right"
            reasons.append("right corridor available")

        return PlanState(
            frame_index=scene_state.frame_index,
            maneuver=maneuver,
            urgency=urgency,
            reasons=reasons,
        )