from __future__ import annotations

from abip.decision.state import DecisionState
from abip.risk.state import RiskState
from abip.scene.state import SceneState


class DecisionEngine:
    def decide(self, scene_state: SceneState, risk_state: RiskState) -> DecisionState:
        reasons: list[str] = []
        action = "continue"
        urgency = "low"

        in_path_objects = [obj for obj in scene_state.objects if obj.is_in_path]

        if risk_state.level == "high":
            action = "brake"
            urgency = "high"
            reasons.append("high scene risk")

        elif risk_state.level == "medium":
            action = "slow_down"
            urgency = "medium"
            reasons.append("moderate scene risk")

        elif risk_state.level == "low":
            action = "slow_down"
            urgency = "medium"
            reasons.append("some nearby objects")

        if in_path_objects:
            nearest = in_path_objects[0]

            if nearest.class_name == "person":
                reasons.append(f"pedestrian in path (ID {nearest.track_id})")
                action = "brake"
                urgency = "high"

            elif nearest.class_name == "car":
                reasons.append(f"vehicle in path (ID {nearest.track_id})")
                action = "brake"
                urgency = "high"

            elif nearest.class_name == "bicycle":
                reasons.append(f"bicycle in path (ID {nearest.track_id})")
                if nearest.horizontal_zone == "left":
                    action = "steer_right"
                    urgency = "medium"
                elif nearest.horizontal_zone == "right":
                    action = "steer_left"
                    urgency = "medium"
                else:
                    action = "slow_down"
                    urgency = "medium"

        if not in_path_objects and risk_state.score < 0.20:
            action = "continue"
            urgency = "low"
            reasons = ["scene appears clear"]

        return DecisionState(
            frame_index=scene_state.frame_index,
            action=action,
            urgency=urgency,
            reasons=reasons,
        )