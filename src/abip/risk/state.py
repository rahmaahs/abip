from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class RiskState:
    frame_index: int
    score: float
    level: str
    reasons: List[str]