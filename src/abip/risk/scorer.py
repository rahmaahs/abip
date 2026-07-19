from __future__ import annotations

from abip.risk.state import RiskState
from abip.scene.state import SceneState


class RiskScorer:
    def __init__(
        self,
        low_threshold: float = 0.30,
        medium_threshold: float = 0.60,
        high_threshold: float = 0.80,
    ) -> None:
        self.low_threshold = low_threshold
        self.medium_threshold = medium_threshold
        self.high_threshold = high_threshold

    def score(self, scene_state: SceneState) -> RiskState:
        score = 0.0
        reasons: list[str] = []

        for obj in scene_state.objects:
            if obj.class_name == "person":
                if obj.is_in_path:
                    score += 0.45
                    reasons.append(f"pedestrian in path (ID {obj.track_id})")
                elif obj.proximity == "mid":
                    score += 0.20
                    reasons.append(f"pedestrian nearby (ID {obj.track_id})")
                elif obj.proximity == "close":
                    score += 0.10
                    reasons.append(f"pedestrian close by (ID {obj.track_id})")

            elif obj.class_name == "car":
                if obj.is_in_path:
                    score += 0.55
                    reasons.append(f"vehicle in path (ID {obj.track_id})")
                elif obj.proximity == "mid":
                    score += 0.25
                    reasons.append(f"vehicle nearby (ID {obj.track_id})")
                elif obj.proximity == "close":
                    score += 0.15
                    reasons.append(f"vehicle close by (ID {obj.track_id})")

            elif obj.class_name == "bicycle":
                if obj.is_in_path:
                    score += 0.25
                    reasons.append(f"bicycle in path (ID {obj.track_id})")
                elif obj.proximity == "mid":
                    score += 0.10
                    reasons.append(f"bicycle nearby (ID {obj.track_id})")

        if scene_state.vehicle_count > 0 and scene_state.pedestrian_count > 0:
            score += 0.10
            reasons.append("mixed traffic near bike")

        score = min(score, 1.0)
        level = self._level_from_score(score)

        if not reasons and score == 0.0:
            reasons.append("scene looks clear")

        return RiskState(
            frame_index=scene_state.frame_index,
            score=score,
            level=level,
            reasons=reasons,
        )

    def _level_from_score(self, score: float) -> str:
        if score >= self.high_threshold:
            return "high"
        if score >= self.medium_threshold:
            return "medium"
        if score >= self.low_threshold:
            return "low"
        return "clear"