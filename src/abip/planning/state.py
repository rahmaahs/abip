from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class PlanState:
    frame_index: int
    maneuver: str
    urgency: str
    reasons: List[str]