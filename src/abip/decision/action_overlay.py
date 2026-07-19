from __future__ import annotations

from typing import Any

import cv2

from abip.decision.state import DecisionState


def draw_decision_overlay(frame: Any, decision_state: DecisionState) -> Any:
    """
    Draw the recommended action on the frame.
    """
    height, width = frame.shape[:2]

    box_width = 520
    box_height = 120
    margin = 20

    x1 = margin
    y1 = height - box_height - margin
    x2 = x1 + box_width
    y2 = y1 + box_height

    color = (0, 255, 0)
    if decision_state.urgency == "medium":
        color = (0, 165, 255)
    elif decision_state.urgency == "high":
        color = (0, 0, 255)

    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness=-1)
    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), thickness=2)

    cv2.putText(
        frame,
        f"ACTION: {decision_state.action.upper()}",
        (x1 + 15, y1 + 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    cv2.putText(
        frame,
        f"Urgency: {decision_state.urgency.upper()}",
        (x1 + 15, y1 + 80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (0, 0, 0),
        2,
        cv2.LINE_AA,
    )

    return frame